import redis

_client = redis.Redis(host="localhost", port=6379, decode_responses=False)

def get_client():
    return _client

def push_snapshot(data: bytes) -> None:
    _client.xadd("vehicle_snapshots", {"payload": data})