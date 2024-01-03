# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

from unittest import IsolatedAsyncioTestCase
from datetime import datetime, timedelta

import redis
import pytest
from preggy import expect
from thumbor.context import Context, RequestParameters
from thumbor.config import Config


from tc_redis.result_storages.redis_result_storage import Storage as RedisStorage
from tests.fixtures.storage_fixtures import IMAGE_URL, IMAGE_BYTES, get_server


class RedisDBContext(IsolatedAsyncioTestCase):
    def setUp(self):
        self.connection = redis.Redis(port=6379, host="localhost", db=0)
        self.cfg = Config(
            REDIS_RESULT_STORAGE_SERVER_HOST="localhost",
            REDIS_RESULT_STORAGE_SERVER_PORT=6379,
            REDIS_RESULT_STORAGE_SERVER_DB=0,
            REDIS_RESULT_STORAGE_SERVER_PASSWORD="",
            RESULT_STORAGE_EXPIRATION_SECONDS=60000,
        )
        self.ctx = Context(
            config=self.cfg,
            server=get_server("ACME-SEC"),
        )
        self.ctx.request = RequestParameters(
            url=IMAGE_URL % 2,
        )
        self.storage = RedisStorage(self.ctx)

    def test_should_be_instance_of_single_node(self):
        expect(str(self.storage.get_storage())).to_equal(
            "Redis<ConnectionPool<Connection<host=localhost,port=6379,db=0>>>"
        )


class CanStoreImage(RedisDBContext):
    def setUp(self):
        super().setUp()

    @pytest.mark.asyncio
    async def test_should_be_in_catalog(self):
        await self.storage.put(IMAGE_BYTES)

        topic = self.connection.get(f"result:{IMAGE_URL % 2}")

        expect(topic).not_to_be_null()
        expect(topic).to_equal(IMAGE_BYTES)


class KnowsImageDoesNotExist(RedisDBContext):
    @pytest.mark.asyncio
    async def test_should_not_exist(self):
        self.ctx.request.url = IMAGE_URL % 10000
        topic = await self.storage.get()
        expect(topic).to_be_null()
        expect(topic).not_to_be_an_error()


class GetMaxAgeFromRedisEnv(RedisDBContext):
    def test_should_get_max_age_from_redis(self):
        self.ctx.request.max_age = 10
        topic = self.storage.get_max_age()
        expect(topic).not_to_be_null()
        expect(topic).to_equal(self.cfg.RESULT_STORAGE_EXPIRATION_SECONDS)


class GetMaxAgeFromRequest(RedisDBContext):
    def test_should_get_max_age_from_request(self):
        max_age = 0
        self.ctx.request.max_age = max_age
        topic = self.storage.get_max_age()
        expect(topic).not_to_be_null()
        expect(topic).to_equal(max_age)


class GetKeyFromRequest(RedisDBContext):
    def test_should_get_key_from_request(self):
        topic = self.storage.get_key_from_request()
        expect(topic).not_to_be_null()
        expect(topic).to_equal(f"result:{self.ctx.request.url}")


class GetWebpKeyFromRequest(RedisDBContext):
    def setUp(self):
        super().setUp()

        self.ctx.config.AUTO_WEBP = True
        self.ctx.request.accepts_webp = True

    def test_should_get_webp_from_request(self):
        topic = self.storage.get_key_from_request()
        expect(topic).not_to_be_null()
        expect(topic).to_equal(f"result:{self.ctx.request.url}/webp")


class CanGetAutoWebp(RedisDBContext):
    def setUp(self):
        super().setUp()

        self.ctx.config.AUTO_WEBP = True
        self.ctx.request.accepts_webp = True

    def test_should_get_auto_webp(self):
        topic = self.storage.get_key_from_request()
        expect(topic).not_to_be_null()
        expect(topic).to_equal(f"result:{self.ctx.request.url}/webp")


class CanNotGetAutoWebp(RedisDBContext):
    def setUp(self):
        super().setUp()

        self.ctx.config.AUTO_WEBP = True
        self.ctx.request.accepts_webp = False

    def test_should_not_get_auto_webp(self):
        topic = self.storage.get_key_from_request()
        expect(topic).not_to_be_null()
        expect(topic).to_equal(f"result:{self.ctx.request.url}")


class CanReadLastUpdatedFromStorage(RedisDBContext):
    def test_should_get_last_updated_from_storage(self):
        self.ctx.request.max_age = 0
        topic = self.storage.last_updated()
        expect(topic).not_to_be_null()
        expect(topic).to_equal(datetime.fromtimestamp(self.storage.start_time))


class CanReadLastUpdatedFromImage(RedisDBContext):
    def test_should_get_last_updated_from_image(self):
        self.connection.set("test_last_updated", IMAGE_BYTES)
        self.connection.expireat(
            "test_last_updated", datetime.now() + timedelta(seconds=1000)
        )
        self.ctx.request.max_age = 10

        topic = self.storage.last_updated()
        expect(topic).not_to_be_null()
        expect(topic).to_be_lesser_than(datetime.now())


class CanReadUnexpiryLastUpdated(RedisDBContext):
    def test_should_get_unexpire_last_updated(self):
        self.connection.set("test_last_updated", IMAGE_BYTES)
        self.ctx.request.max_age = 10
        ttl = self.connection.ttl("test_last_updated")
        topic = self.storage.last_updated()
        expect(topic).not_to_be_null()
        expect(ttl).to_equal(-1)


class CanRaiseErrors(RedisDBContext):
    @pytest.mark.asyncio
    async def test_should_throw_an_exception(self):
        config = Config(
            REDIS_RESULT_STORAGE_SERVER_HOST="localhost",
            REDIS_RESULT_STORAGE_SERVER_PORT=300,
            REDIS_RESULT_STORAGE_SERVER_DB=0,
            REDIS_RESULT_STORAGE_SERVER_PASSWORD="nope",
            REDIS_RESULT_STORAGE_IGNORE_ERRORS=False,
        )
        ctx = Context(
            config=config,
            server=get_server("ACME-SEC"),
        )
        ctx.request = RequestParameters(
            url=IMAGE_URL,
        )
        storage = RedisStorage(
            context=ctx,
            shared_client=False,
        )

        try:
            topic = await storage.get()
        except Exception as redis_error:
            expect(redis_error).not_to_be_null()
            expect(redis_error).to_be_an_error_like(redis.RedisError)


class CanIgnoreErrors(RedisDBContext):
    @pytest.mark.asyncio
    async def test_should_not_throw_an_exception(self):
        cfg = Config(
            REDIS_RESULT_STORAGE_SERVER_HOST="localhost",
            REDIS_RESULT_STORAGE_SERVER_PORT=300,
            REDIS_RESULT_STORAGE_SERVER_DB=0,
            REDIS_RESULT_STORAGE_SERVER_PASSWORD="nope",
            REDIS_RESULT_STORAGE_IGNORE_ERRORS=True,
        )
        ctx = Context(
            config=cfg,
            server=get_server("ACME-SEC"),
        )
        ctx.request = RequestParameters(
            url=IMAGE_URL % 10,
        )
        storage = RedisStorage(
            context=ctx,
            shared_client=False,
        )

        topic = await storage.get()
        expect(topic).to_equal(None)
        expect(topic).not_to_be_an_error()


class ConnectToRedisWithoutPassword(RedisDBContext):
    def setUp(self):
        super().setUp()

        self.cfg = Config(
            REDIS_RESULT_STORAGE_SERVER_HOST="localhost",
            REDIS_RESULT_STORAGE_SERVER_PORT=6379,
            REDIS_RESULT_STORAGE_SERVER_DB=0,
        )
        self.ctx = Context(
            config=self.cfg,
            server=get_server("ACME-SEC"),
        )
        self.ctx.request = RequestParameters(
            url=IMAGE_URL % 2,
        )
        self.storage = RedisStorage(self.ctx)

    @pytest.mark.asyncio
    async def test_should_be_in_catalog(self):
        await self.storage.put(IMAGE_BYTES)

        topic = self.connection.get(f"result:{IMAGE_URL % 2}")

        expect(topic).not_to_be_null()
        expect(topic).not_to_be_an_error()


class RedisModeInvalid(RedisDBContext):
    def setUp(self):
        super().setUp()

        self.cfg = Config(
            REDIS_RESULT_STORAGE_SERVER_HOST="localhost",
            REDIS_RESULT_STORAGE_SERVER_PORT=6379,
            REDIS_RESULT_STORAGE_SERVER_DB=0,
            REDIS_RESULT_STORAGE_MODE="test",
        )
        self.ctx = Context(
            config=self.cfg,
            server=get_server("ACME-SEC"),
        )
        self.ctx.request = RequestParameters(
            url=IMAGE_URL % 2,
        )

    @pytest.mark.asyncio
    async def test_should_raises_attribute_error(self):
        with self.assertRaises(AttributeError) as error:
            RedisStorage(self.ctx)

        expect(str(error.exception)).to_equal(
            "Unknown value for REDIS_RESULT_STORAGE_MODE test. See README for more information."
        )
