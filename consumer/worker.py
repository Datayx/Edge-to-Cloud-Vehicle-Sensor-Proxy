import redis
from consumer.db import get_connection, setup, insert
from ingest.schema import snapshot_pb2

STREAM = "vehicle_snapshots"
GROUP  = "consumer_group"
WORKER = "worker_1"

r = redis.Redis(host="localhost", port=6379, decode_responses=False)

def ensure_group():
    try:
        r.xgroup_create(STREAM, GROUP, id="0", mkstream=True)
    except redis.exceptions.ResponseError:
        pass

def process():
    conn = get_connection()
    setup(conn)
    ensure_group()

    while True:
        r.xautoclaim(STREAM, GROUP, WORKER, min_idle_time=60000, start_id="0-0")

        messages = r.xreadgroup(GROUP, WORKER, {STREAM: ">"}, count=100, block=1000)
        if not messages:
            continue

        for _, entries in messages:
            for msg_id, data in entries:
                snapshot = snapshot_pb2.SensorSnapshot()
                snapshot.ParseFromString(data[b"payload"])
                insert(conn, snapshot)
                r.xack(STREAM, GROUP, msg_id)
                print(f"✅ Processed: {snapshot.vehicle_id} to the {snapshot.timestamp_ms}")

if __name__ == "__main__":
    process()