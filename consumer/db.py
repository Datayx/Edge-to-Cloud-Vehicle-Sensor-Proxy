import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="telemetry", user="dev", password="dev", host="localhost"
    )

def setup(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS snapshots (
                vehicle_id   TEXT,
                timestamp_ms BIGINT,
                speed_ms     FLOAT,
                battery_pct  FLOAT,
                motor_temp_c FLOAT,
                imu_accel    FLOAT[],
                PRIMARY KEY (vehicle_id, timestamp_ms)
            )
        """)
    conn.commit()

def insert(conn, snapshot):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO snapshots VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (
            snapshot.vehicle_id,
            snapshot.timestamp_ms,
            snapshot.speed_ms,
            snapshot.battery_pct,
            snapshot.motor_temp_c,
            snapshot.imu_accel[:]
        ))
    conn.commit()