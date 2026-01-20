import { useEffect, useState } from "react";
import { getStats, csvURL } from "../services/api";

export default function StatsPanel() {
  const [stats, setStats] = useState({
    people: 0,
    vehicles: 0,
    line_crossed: 0,
    fps: 0
  });

  useEffect(() => {
    const timer = setInterval(async () => {
      const data = await getStats();
      setStats(data);
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  return (
    <div style={{ border: "1px solid #ccc", padding: "15px", width: "300px" }}>
      <h2>Realtime Analytics</h2>
      <p>👤 People: {stats.people}</p>
      <p>🚗 Vehicles: {stats.vehicles}</p>
      <p>🚦 Line Crossed: {stats.line_crossed}</p>
      <p>⚡ FPS: {stats.fps}</p>

      <a href={csvURL} target="_blank" rel="noopener noreferrer">
        <button style={{ marginTop: "10px" }}>
          ⬇ Download CSV
        </button>
      </a>
    </div>
  );
}
