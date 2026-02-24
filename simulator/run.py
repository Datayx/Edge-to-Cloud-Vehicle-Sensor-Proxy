import asyncio
import time
import random
import httpx
import argparse
import sys
sys.path.append(".")
from ingest.schema import snapshot_pb2

async def emit(client: httpx.AsyncClient, vehicle_id: str, hz: int):
    interval = 1.0 / hz
    while True:
        start_time = time.time()
        
        snapshot = snapshot_pb2.SensorSnapshot(
            vehicle_id=vehicle_id,
            timestamp_ms=int(start_time * 1000),
            speed_ms=random.uniform(0, 40),
            battery_pct=random.uniform(20, 100),
            motor_temp_c=random.uniform(30, 90),
            imu_accel=[random.uniform(-1, 1) for _ in range(3)]
        )
        
        try:
            response = await client.post(
                "http://localhost:8000/ingest",
                content=snapshot.SerializeToString(),
                headers={"Content-Type": "application/octet-stream"}
            )
            response.raise_for_status()
        except Exception as e:
            print(f"[{vehicle_id}] Drop of conection: {e}")
        
        elapsed = time.time() - start_time
        sleep_time = max(0.0, interval - elapsed)
        await asyncio.sleep(sleep_time)

async def main(vehicles: int, hz: int):
    async with httpx.AsyncClient() as client:
        tasks = [emit(client, f"vehicle_{i}", hz) for i in range(vehicles)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--vehicles", type=int, default=5)
    parser.add_argument("--hz", type=int, default=10)
    args = parser.parse_args()
    try:
        asyncio.run(main(args.vehicles, args.hz))
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        input("Press enter to exit")
