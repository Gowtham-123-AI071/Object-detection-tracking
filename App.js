import { useEffect, useRef, useState } from "react";

const backend = "http://127.0.0.1:8000";

function App() {
  const [data, setData] = useState([]);
  const canvasRef = useRef(null);

  useEffect(() => {
    fetch(`${backend}/analytics/json`)
      .then(res => res.json())
      .then(setData);
  }, []);

  useEffect(() => {
    if (!data.length) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const points = data[data.length - 1].heatmap;

    points.forEach(p => {
      ctx.fillStyle = "rgba(255,0,0,0.05)";
      ctx.beginPath();
      ctx.arc(p.x, p.y, 8, 0, 2 * Math.PI);
      ctx.fill();
    });
  }, [data]);

  return (
    <div style={{ padding: 30 }}>
      <h1>📊 Object Tracking Dashboard</h1>

      <a href={`${backend}/analytics/csv`}>
        <button>Download CSV</button>
      </a>

      <h3>Session Summary</h3>
      <p>Total frames: {data.length}</p>

      <h3>🔥 Heatmap</h3>
      <canvas ref={canvasRef} width={640} height={480} style={{ border: "1px solid black" }} />
    </div>
  );
}

export default App;
