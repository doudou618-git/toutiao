import json
import os
from typing import Any

import redis.asyncio as redis

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
REDIS_DB = int(os.environ.get("REDIS_DB", "0"))


#创建Redis的连接对象
redis_client = redis.Redis(
    host=REDIS_HOST,  #Redis服务器的主机地址
    port=REDIS_PORT,   #Redis端口号
    db=REDIS_DB,   #Redis数据库编号 0-15
    decode_responses=True   #是否将字节数据解码为字符串
)
#读取字符串
async def get_cache(key: str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败: {e}")
        return None

#读取列表或者字典
async def get_json_cache(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f"获取JSON缓存失败: {e}")
        return None


#设置缓存
async def set_cache(key: str, value: Any, expire: int = 3600):
    try:
        if isinstance(value , (list , dict)):  #转字符串再存
            value = json.dumps(value , ensure_ascii=False)#设置中文正常保存
        await redis_client.setex(key , expire ,  value)
        return True
    except Exception as e:
        print(f"设置缓存失败: {e}")
        return False
