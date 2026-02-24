from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect
from ingest.redis_client import push_snapshot, get_client
from ingest.schema import snapshot_pb2
import asyncio
import json


app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

connected_clients: list[WebSocket] = []

@app.post("/ingest")
async def ingest(request: Request):
    body = await request.body()
    if not body:
        raise HTTPException(status_code=400, detail="Empty body")
    push_snapshot(body)
    return {"status": "ok"}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    connected_clients.append(ws)
    try:
        while True:
            await asyncio.sleep(10)  # keep alive
    except WebSocketDisconnect:
        connected_clients.remove(ws)

@app.on_event("startup")
async def start_stream_broadcaster():
    asyncio.create_task(broadcast_stream())

async def broadcast_stream():
    r = get_client()
    last_id = "$"
    while True:
        messages = await asyncio.to_thread(
            r.xread, {"vehicle_snapshots": last_id}, 10, 100
        )
        if messages:
            for _, entries in messages:
                for msg_id, data in entries:
                    last_id = msg_id
                    snapshot = snapshot_pb2.SensorSnapshot()
                    snapshot.ParseFromString(data[b"payload"])
                    payload = json.dumps({
                        "vehicle_id":   snapshot.vehicle_id,
                        "timestamp_ms": snapshot.timestamp_ms,
                        "speed_ms":     snapshot.speed_ms,
                        "battery_pct":  snapshot.battery_pct,
                        "motor_temp_c": snapshot.motor_temp_c,
                        "imu_accel":    list(snapshot.imu_accel)
                    })
                    dead = []
                    for client in connected_clients:
                        try:
                            await client.send_text(payload)
                        except Exception:
                            dead.append(client)
                    for d in dead:
                        connected_clients.remove(d)
        await asyncio.sleep(0.01)
    
@app.get("/stream-lag")
async def stream_lag():
    r = get_client()
    lag = await asyncio.to_thread(r.xlen, "vehicle_snapshots")
    return {"lag": lag}

@app.post("/consumer/pause")
async def pause_consumer():
    import subprocess
    subprocess.Popen(["docker", "stop", "edgelink-proxy-consumer-1"])
    return {"status": "paused"}

@app.post("/consumer/resume")
async def resume_consumer():
    import subprocess
    subprocess.Popen(["docker", "start", "edgelink-proxy-consumer-1"])
    return {"status": "resumed"}
