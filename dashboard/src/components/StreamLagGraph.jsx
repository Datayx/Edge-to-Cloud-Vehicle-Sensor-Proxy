import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export function StreamLagGraph() {
    const [lag, setLag] = useState([]);

    useEffect(() => {
        const interval = setInterval(async () => {
            const res = await fetch("http://localhost:8000/stream-lag");
            const data = await res.json();
            setLag(prev => [...prev.slice(-50), { time: Date.now(), lag: data.lag }]);
        }, 1000);
        return () => clearInterval(interval);
    }, []);

    return (
        <ResponsiveContainer width="100%" height={200}>
            <LineChart data={lag}>
                <XAxis dataKey="time" hide />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="lag" stroke="#ff4444" dot={false} />
            </LineChart>
        </ResponsiveContainer>
    );
}