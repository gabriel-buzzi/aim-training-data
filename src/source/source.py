import cv2
import pandas as pd
from datetime import datetime, timedelta

# Video file path
VIDEO_FILE_PATH = "task.mp4"

# Parameters for the center crop
CROP_WIDTH = 500  # Adjust based on your video resolution
CROP_HEIGHT = 500

def crop_center(frame, crop_width, crop_height):
    """Crop the center of the frame."""
    h, w = frame.shape[:2]
    start_x = (w - crop_width) // 2
    start_y = (h - crop_height) // 2
    return frame[start_y:start_y + crop_height, start_x:start_x + crop_width]

def track_white_object(video_path, crop_width, crop_height):
    # Load video and initialize output data
    cap = cv2.VideoCapture(video_path)
    
    # Get video FPS to calculate timestamps
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Frames per second (FPS): {fps}")

    # Record the system datetime when processing starts
    start_time = datetime.now()
    print(f"Video processing start time: {start_time}")

    positions = []

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # Exit at the end of the video

        # Calculate timestamp: system datetime incremented by frame_count / fps
        current_datetime = start_time + timedelta(seconds=frame_count / fps)

        # Center crop the frame
        cropped_frame = crop_center(frame, crop_width, crop_height)
        
        # Convert the frame to grayscale
        gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
        
        # Threshold to isolate the white object (bright regions)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

        # Find contours to detect object
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Find the largest contour (assuming the white object is the largest)
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Get the center of the contour
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:  # Avoid division by zero
                cx = int(M["m10"] / M["m00"])  # X-coordinate of center
                cy = int(M["m01"] / M["m00"])  # Y-coordinate of center
                
                # Get bounding box of the contour
                x, y, w, h = cv2.boundingRect(largest_contour)
                
                # Append frame number, datetime, center, and bounding box coordinates
                positions.append((frame_count, current_datetime, cx, cy, x, y, w, h))

                # Draw the center and bounding box for visualization (optional)
                cv2.circle(cropped_frame, (cx, cy), 5, (0, 0, 255), -1)  # Center
                cv2.rectangle(cropped_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Bounding box

        # Optional: Show the frame for debugging
        cv2.imshow("Tracking", cropped_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        frame_count += 1

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    
    # Save positions to CSV
    df = pd.DataFrame(positions, columns=[
        "Frame", "Datetime", "Center_X", "Center_Y", "Box_X", "Box_Y", "Box_Width", "Box_Height"
    ])
    df.to_csv("tracked_positions.csv", index=False)
    print("Tracking complete! Positions saved to 'tracked_positions.csv'.")

if __name__ == "__main__":
    track_white_object(VIDEO_FILE_PATH, CROP_WIDTH, CROP_HEIGHT)
