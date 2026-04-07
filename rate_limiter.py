import redis
import time

r = redis.Redis(host='localhost', port=6379, db=1)

RATE_LIMIT = 3  # requests per second
KEY = "api_tokens"

def refill_tokens():
    current_time = int(time.time())
    last_refill = r.get("last_refill")

    if not last_refill:
        r.set("last_refill", current_time)
        r.set(KEY, RATE_LIMIT)
        return

    if current_time > int(last_refill):
        r.set(KEY, RATE_LIMIT)
        r.set("last_refill", current_time)


def consume_token():
    refill_tokens()
    tokens = int(r.get(KEY) or 0)

    if tokens > 0:
        r.decr(KEY)
        return True
    return False
