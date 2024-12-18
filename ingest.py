import cv2
from ultralytics import YOLO

# Load YOLO11 model
model = YOLO("yolo11n.pt")

# Open the video file
video_path = "cropped_task.mp4"
cap = cv2.VideoCapture(video_path)

positions = []

# Loop through video frames
while cap.isOpened():
    success, frame = cap.read()
    if success:
        # Preprocess for stability
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        
        # Track with adjusted parameters
        results = model.track(frame, conf=0.2, iou=0.1, persist=True)

        # Handle object loss (optional re-detection fallback)
        if len(results) == 0:
            results = model.predict(frame, conf=0.3)

        positions.append(results)

        # Visualize annotated frame
        annotated_frame = results[0].plot()

        # Display output
        cv2.imshow("YOLO11 Tracking", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()

print(positions)