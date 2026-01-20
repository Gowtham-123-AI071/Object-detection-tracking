import { videoURL } from "../services/api";

export default function VideoFeed() {
  return (
    <div>
      <h2>Live Video Stream</h2>
      <img
        src={videoURL}
        alt="Live Stream"
        width="640"
        style={{ border: "2px solid black" }}
      />
    </div>
  );
}
