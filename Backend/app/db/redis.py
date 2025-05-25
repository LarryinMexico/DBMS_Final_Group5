import redis.asyncio as redis

REDIS_URL = 'rediss://default:AZ0LAAIjcDE4YjU0ZTlhZDllNDY0NDE1YTViYTk2NDI3Y2ZiNDY2NXAxMA@ready-impala-40203.upstash.io:6379'

redis_client = redis.from_url(REDIS_URL, decode_responses=True)
