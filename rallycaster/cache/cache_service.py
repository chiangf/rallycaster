"""
Defines the wrapper to the cache. The cache implementation currently used is Redis.
"""

import redis
import cPickle
from rallycaster import app
from rallycaster.interfaces.error_handling import DataException


# If no timeout is specified, this default timeout value will be set. When the redis key expires,
# the key will disappear automatically.
DEFAULT_EXPIRE_TIMEOUT_IN_SECS = 86400  # 1 day in seconds


def get_redis_connection():
    """
    Creates a Redis instance that will be used to talk with Redis. This instance creates a connection
    pool that will be used for all calls by the CacheService class.

    Reason that this instantiated at module-level: Module instantiation happens only at the first time
       when the module is imported during a process. Therefore, there will only be 1 redis instance for
       a process.

    @return: Redis connection object.
    """
    connection = redis.StrictRedis(host=app.config['REDIS']['host'], port=app.config['REDIS']['port'])
    return connection


class CacheService(object):
    """Handles reading, writing to cache

    Usage:
      store = CacheService()
      store.set("key", "value")
      val = store.get("key")    # val will contain "value"

    Transactions:
      store = CacheService()
      store.start_pipe()
      store.set("key", "value")
      store.get("key")
      val = store.execute_pipe()    # val will contain [True, "value"]

    Serialization (cPickle):
      To store objects into the cache, we use cPickle to serialize the object into a string, which
      is an implementation of pickle written in C. From performance tests, serialization takes
      a little longer than json.dumps (with a special encoder for complex objects) but
      deserialization is much faster. Since deserialization is more important, cPickle is the
      clear winner.
    """

    def __init__(self):
        self.__pipe = None

    def start_pipe(self, transaction=True):
        """Starts transaction and all subsequent calls to this service will be buffered"""
        if self.is_pipe_started():
            raise DataException("Existing pipe found when starting a new pipe. Call execute_pipe() on existing pipe.")

        self.__pipe = _store.pipeline(transaction=transaction)

    def execute_pipe(self):
        """Ends transaction and all buffered calls will be executed"""
        ret_list = self.__pipe.execute()
        self.__pipe = None

        # Must decode results from get() because usually it is decoded in the get()
        # call but since pipelines execute at the end, we need to do that as well.
        for index, value in enumerate(ret_list):
            ret_list[index] = self._decode_value(value)

        return ret_list

    def is_pipe_started(self):
        if self.__pipe:
            return True
        else:
            return False

    def __context_obj(self):
        """Gets context object to act on:
        If pipe has been started (via start_pipe), return the pipe. Otherwise, return the redis object.
        """
        if self.is_pipe_started():
            return self.__pipe
        else:
            return _store

    def exist(self, key):
        return self.__context_obj().exists(key)

    def set(self, key, value, expire_in_seconds=DEFAULT_EXPIRE_TIMEOUT_IN_SECS, encode_value=True):
        """
        Gets value from cache.

        Note: encode_value is only used to share keys between PHP and Python (because PHP
            does not know how to pickle). Remove this afterwards.
        """

        if encode_value:
            serialized_value = cPickle.dumps(value)
        else:
            serialized_value = value

        key = self._normalize_key(key)

        if not expire_in_seconds:
            self.__context_obj().set(key, serialized_value)
        else:
            self.__context_obj().setex(key, expire_in_seconds, serialized_value)

    def hset(self, key, hash_key, hash_value, expire_in_seconds=DEFAULT_EXPIRE_TIMEOUT_IN_SECS):
        key = self._normalize_key(key)
        self.__context_obj().hset(key, hash_key, hash_value)

        self.expire(key, expire_in_seconds)

    def hmset(self, key, hash_dict, expire_in_seconds=DEFAULT_EXPIRE_TIMEOUT_IN_SECS):
        """
        Sets multiple keys/values for a hash key.

        Example: hmset('foo', {'bar':123, 'baz':234}) will store hash keys 'bar' and 'baz' into cache key 'foo'.
        """
        key = self._normalize_key(key)
        self.__context_obj().hmset(key, hash_dict)

        self.expire(key, expire_in_seconds)

    def hsetlpush(self, key, hash_key, value_to_append, expire_in_seconds=DEFAULT_EXPIRE_TIMEOUT_IN_SECS):
        """
        Pushes a value onto a list inside a hash key. If the list does not exist yet, initializes
        a new list.
        """
        serialized_list = self.__context_obj().hget(key, hash_key)
        if serialized_list is None:
            deserialized_list = []
        else:
            deserialized_list = cPickle.loads(serialized_list)

        key = self._normalize_key(key)

        # Append the new job to the list of chained jobs and put it back into redis
        deserialized_list.append(value_to_append)
        serialized_list = cPickle.dumps(deserialized_list)
        self.__context_obj().hset(key, hash_key, serialized_list)

        self.expire(key, expire_in_seconds)

    def hget(self, key, hash_key):
        return self.__context_obj().hget(key, hash_key)

    def hmget(self, key, hash_key, *args):
        """
        Gets multiple key values for a hash key.

        @param key: Key to get from cache
        @param hash_key: First hash key to get value
        @param args: Optional list of other hash keys to get values
        """
        return self.__context_obj().hmget(key, hash_key, *args)

    def hgetall(self, key):
        return self.__context_obj().hgetall(key)

    def hdel(self, key, *hash_keys):
        self.__context_obj().hdel(key, *hash_keys)

    def lpush(self, key, *values):
        """Pushes values onto list object in the cache"""
        ret = self.__context_obj().lpush(key, *values)
        return ret

    def llen(self, key):
        """Gets length of list object in the cache"""
        ret = self.__context_obj().llen(key)
        return ret

    def get(self, key, decode_value=True):
        """
        Gets value from cache.

        Note: decode_value is only used to share keys between PHP and Python (because PHP
            does not know how to pickle). Remove this afterwards.
        """

        ret = self.__context_obj().get(key)

        if decode_value:
            return self._decode_value(ret)
        else:
            return ret

    def keys(self, pattern='*'):
        return self.__context_obj().keys(pattern)

    def expire(self, key, expire_in_seconds=0):
        self.__context_obj().expire(key, expire_in_seconds)

    def lock(self, key, timeout=None, sleep=0.1):
        return self.__context_obj().lock(key, timeout, sleep)

    def _normalize_key(self, key):
        return "{0}:{1}".format(app.config['REDIS']['key_prefix'], key)

    def _decode_value(self, value):
        if isinstance(value, basestring):
            return cPickle.loads(value)
        else:
            return value


_store = get_redis_connection()     # pylint: disable=C0103
cache = CacheService()         # pylint: disable=C0103
