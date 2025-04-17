import redis.asyncio as redis

class RedisConnectionManager:
    def __init__(self, redis_url="redis://localhost:6379"):
        self.redis = redis.Redis.from_url(redis_url)

    async def set_user_channel(self, user_id: int, channel_name: str, ttl: int = 3600):
        key = f"user:{user_id}"
        await self.redis.set(key, channel_name, ex=ttl)

    async def get_user_channel(self, user_id: int) -> str | None:
        key = f"user:{user_id}"
        return await self.redis.get(key, encoding="utf-8")

    async def delete_user_channel(self, user_id: int):
        key = f"user:{user_id}"
        await self.redis.delete(key)

    async def user_channel_exists(self, user_id: int) -> bool:
        key = f"user:{user_id}"
        return await self.redis.exists(key) > 0