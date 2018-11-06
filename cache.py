import redis

class RedisCache(object):
    redis_db = redis.StrictRedis(host='localhost', port=6379, db=5)

    def set(self, key, value):
        return RedisCache.redis_db.set(key, value)

    def get(self, key):
        return RedisCache.redis_db.get(key)

    def keys(self, key):
        return RedisCache.redis_db.keys(key)

    def lpush(self, key, value):
        return RedisCache.redis_db.lpush(key, value)

    def sadd(self, key, value):
        return RedisCache.redis_db.sadd(key, value)

    def smembers(self, key):
        return RedisCache.redis_db.smembers(key)

    # 命令判断成员元素是否是集合的成员
    def sismember(self, key, value):
        return RedisCache.redis_db.sismember(key, value)

    # 用于移除集合中的一个或多个成员元素，不存在的成员元素会被忽略
    def srem(self, key, value):
        return RedisCache.redis_db.srem(key, value)
    

