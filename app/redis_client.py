import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

def get_cached(key: str):
    try:
        data = r.get(key)
        if data:
            return json.loads(data)
        return None
    except redis.RedisError as e:
        print(f"Redis get error: {e}")
        return None

def set_cache(key: str, value, ttl=300):  
    try:
        r.setex(key, ttl, json.dumps(value))
    except redis.RedisError as e:
        print(f"Redis set error: {e}")

def delete_cache(key: str):
    try:
        r.delete(key)
    except redis.RedisError as e:
        print(f"Redis delete error: {e}")

def clear_search_cache():
    try:
        keys = r.keys("*")
        search_keys = [key for key in keys if key.islower() and len(key) > 0]
        if search_keys:
            r.delete(*search_keys)
    except redis.RedisError as e:
        print(f"Redis clear cache error: {e}")

def invalidate_movie_cache(movie_title: str):
    try:
        keys = r.keys("*")
        for key in keys:
            if movie_title.lower() in key.lower():
                r.delete(key)
    except redis.RedisError as e:
        print(f"Redis invalidation error: {e}")
