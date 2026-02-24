from locust import HttpUser, task, between
import time
import random
import sys
sys.path.append(".")
from ingest.schema import snapshot_pb2

class VehicleUser(HttpUser):
    wait_time = between(0.05, 0.1)  # ~10Hz per vehicle

    @task
    def send_snapshot(self):
        snapshot = snapshot_pb2.SensorSnapshot(
            vehicle_id=f"load_vehicle_{self.user_id if hasattr(self, 'user_id') else 0}",
            timestamp_ms=int(time.time() * 1000),
            speed_ms=random.uniform(0, 40),
            battery_pct=random.uniform(20, 100),
            motor_temp_c=random.uniform(30, 90),
            imu_accel=[random.uniform(-1, 1) for _ in range(3)]
        )
        self.client.post(
            "/ingest",
            data=snapshot.SerializeToString(),
            headers={"Content-Type": "application/octet-stream"}
        )