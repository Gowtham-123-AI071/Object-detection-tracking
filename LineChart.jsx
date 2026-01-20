import { LineChart, Line, XAxis, YAxis, Tooltip } from "recharts";
import { useEffect, useState } from "react";

export default function LineCrossChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/analytics/json")
      .then(res => res.json())
      .then(setData);
  }, []);

  return (
    <div>
      <h2>Line Crossing Trend</h2>
      <LineChart width={600} height={300} data={data}>
        <XAxis dataKey="timestamp" hide />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="line_crossed" stroke="#ff0000" />
      </LineChart>
    </div>
  );
}
