import cv2
def overlay_heatmap(frame, heatmap):
    heat = cv2.resize(heatmap, (frame.shape[1], frame.shape[0]))
    heat = (heat * 255).astype("uint8")
    heat = cv2.applyColorMap(heat, cv2.COLORMAP_JET)
    return cv2.addWeighted(frame, 0.6, heat, 0.4, 0)

def draw_dashboard(frame, tracked, people, vehicles, crossed, fps, line_y):
    h, w, _ = frame.shape
    cv2.line(frame, (0, line_y), (w, line_y), (0,0,255), 2)

    for obj in tracked:
        x1, y1, x2, y2 = obj["bbox"]
        tid = obj["id"]
        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
        cv2.putText(frame, f"ID {tid}", (x1,y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    cv2.rectangle(frame, (10,10), (360,160), (0,0,0), -1)
    cv2.putText(frame, f"People: {people}", (20,40), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(255,255,255),2)
    cv2.putText(frame, f"Vehicles: {vehicles}", (20,70), cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)
    cv2.putText(frame, f"Crossed Line: {crossed}", (20,100), cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)
    cv2.putText(frame, f"FPS: {int(fps)}", (20,130), cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)

    return frame
