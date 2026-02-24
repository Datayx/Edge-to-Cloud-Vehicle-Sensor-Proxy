import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";

export function SensorChart({ data }) {
    return (
        <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data}>
                <XAxis dataKey="timestamp_ms" hide />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="speed_ms" stroke="#8884d8" dot={false} />
                <Line type="monotone" dataKey="battery_pct" stroke="#82ca9d" dot={false} />
                <Line type="monotone" dataKey="motor_temp_c" stroke="#ff7300" dot={false} />
            </LineChart>
        </ResponsiveContainer>
    );
}