import { useState } from "react";
import { useWebSocket } from "./hooks/useWebSocket";
import { VehicleSelector } from "./components/VehicleSelector";
import { SensorChart } from "./components/SensorChart";
import { StreamLagGraph } from "./components/StreamLagGraph";
import { FaultInjector } from "./components/FaultInjector";

function App() {
    const snapshots = useWebSocket("ws://localhost:8000/ws");
    const [selected, setSelected] = useState(null);

    const vehicles = Object.keys(snapshots);
    const selectedData = selected ? snapshots[selected] : [];

    return (
        <div style={{ padding: 24, fontFamily: "monospace" }}>
            <h1>EdgeLink Proxy — Live Telemetry</h1>

            <h2>Vehicles</h2>
            <VehicleSelector vehicles={vehicles} selected={selected} onSelect={setSelected} />

            <h2>Sensor Readings — {selected || "select a vehicle"}</h2>
            <SensorChart data={selectedData} />

            <h2>Stream Lag</h2>
            <StreamLagGraph />

            <FaultInjector />
        </div>
    );
}

export default App;