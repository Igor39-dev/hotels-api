from src.connectors.redis_connector import RedisManager
from src.config import settings


redis_manager = RedisManager(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

# async def init_connectors():
#     await redis_manager.connect()

# async def close_connectors():
#     await redis_manager.close()

# async def get_redis_manager():
#     return redis_manager
