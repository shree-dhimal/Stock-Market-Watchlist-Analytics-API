from .base import *
from common_utils.cache.backends import get_redis_cache_config
from decouple import config

DEBUG = False

SESSION_COOKIE_SECURE = True  # True in prod (HTTPS)
    
CACHES = get_redis_cache_config(host=config("REDIS_HOST","127.0.0.1"),port=config("REDIS_PORT",6379), db=config("REDIS_DB",1),timeout=config("REDIS_TIMEOUT",300))