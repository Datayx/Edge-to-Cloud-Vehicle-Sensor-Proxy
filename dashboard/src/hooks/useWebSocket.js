import { useEffect, useRef, useState } from "react";

export function useWebSocket(url) {
    const [snapshots, setSnapshots] = useState({});
    const ws = useRef(null);

    useEffect(() => {
        ws.current = new WebSocket(url);
        ws.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setSnapshots(prev => ({
                ...prev,
                [data.vehicle_id]: [
                    ...(prev[data.vehicle_id] || []).slice(-50),
                    data
                ]
            }));
        };
        return () => ws.current.close();
    }, [url]);

    return snapshots;
}