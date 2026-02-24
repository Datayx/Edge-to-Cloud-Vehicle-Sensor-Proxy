import { useState } from "react";

export function FaultInjector() {
    const [paused, setPaused] = useState(false);

    const toggle = async () => {
        const endpoint = paused ? "resume" : "pause";
        await fetch(`http://localhost:8000/consumer/${endpoint}`, { method: "POST" });
        setPaused(!paused);
    };

    return (
        <div>
            <h3>Fault Injection</h3>
            <button onClick={toggle} style={{ background: paused ? "#ff4444" : "#44ff44", padding: 8 }}>
                {paused ? "Resume Consumer" : "Pause Consumer"}
            </button>
            {paused && <p style={{ color: "red" }}>Consumer paused — watch lag spike above</p>}
        </div>
    );
}