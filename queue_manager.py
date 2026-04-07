import redis
import json

r = redis.Redis(host='localhost', port=6379, db=2)

def add_request(customer_id, payload):
    key = f"queue:{customer_id}"
    r.rpush(key, json.dumps(payload))

def get_all_customers():
    keys = r.keys("queue:*")
    return [k.decode().split(":")[1] for k in keys]

def pop_request(customer_id):
    key = f"queue:{customer_id}"
    data = r.lpop(key)
    return json.loads(data) if data else None
