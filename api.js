const API_BASE = "http://127.0.0.1:8000";

export const videoURL = `${API_BASE}/video`;

export async function getStats() {
  const res = await fetch(`${API_BASE}/stats`);
  return res.json();
}

export const csvURL = `${API_BASE}/analytics/csv`;
