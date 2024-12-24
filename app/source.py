import cv2
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import os
import numpy as np

# Video path
VIDEO_FILE_PATH = "example.mp4"

# Matadata
TASK_ID = '1'
USER_ID = '1'
DATASET_PATH = os.path.join(
    '/home',
    'gabriel',
    'code',
    'aim-training-data',
    'data'
)

# Parameters for the center crop
CROP_WIDTH = 500  # Adjust based on your video resolution
CROP_HEIGHT = 500

def crop_center(frame, crop_width, crop_height):
    """Crop the center of the frame."""
    h, w = frame.shape[:2]
    start_x = (w - crop_width) // 2
    start_y = (h - crop_height) // 2
    return frame[start_y:start_y + crop_height, start_x:start_x + crop_width]

def track_white_object(video_path, crop_width, crop_height, output_folder):

    # Load video and initialize output data
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Adjust the dimensions for cropped frames
    output_width = min(crop_width, frame_width)
    output_height = min(crop_height, frame_height)

    # Initialize video writer for saving processed video
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec for MP4
    out = cv2.VideoWriter(os.path.join(output_folder, "video.mp4"), fourcc, fps, (output_width, output_height))

    # Record the system datetime when processing starts
    start_time = datetime.now()

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
        
        row = (TASK_ID, USER_ID, frame_count, fps, current_datetime, CROP_WIDTH, CROP_HEIGHT, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan)

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
                
                # Update frame number, datetime, center, and bounding box coordinates when target is find
                row = (TASK_ID, USER_ID, frame_count, fps, current_datetime, CROP_WIDTH, CROP_HEIGHT, cx, cy, x, y, w, h)
                
                # Draw the center and bounding box for visualization
                cv2.circle(cropped_frame, (cx, cy), 5, (0, 0, 255), -1)  # Center
                #cv2.circle(cropped_frame, (x, y), 5, (0, 0, 255), -1)
                cv2.rectangle(cropped_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Bounding box

        # Append frame number, datetime, center, and bounding box coordinates
        positions.append(row)

        # Write the processed frame to the output video
        out.write(cropped_frame)

        # Optional: Show the frame for debugging
        cv2.imshow("Tracking", cropped_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        frame_count += 1

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # Create a dataframe with position data 
    df = pd.DataFrame(positions, columns=[
        "Task_ID", "User_ID", "Frame", "FPS", "Datetime", "Video_Width", "Video_Height", "Center_X", "Center_Y", "Box_X", "Box_Y", "Box_Width", "Box_Height"
    ])

    # Save positions to CSV in the output folder
    output_csv_path = os.path.join(output_folder, "data.csv")
    df.to_csv(output_csv_path, index=False)
    print(f"Tracking complete! Positions saved to '{output_csv_path}' and video saved to '{output_video_path}'.")


if __name__ == "__main__":
    
    output_folder = os.path.join(
        DATASET_PATH,
        TASK_ID,
        'source'
    )

    os.makedirs(output_folder, exist_ok=True)

    track_white_object(
        VIDEO_FILE_PATH, 
        CROP_WIDTH, 
        CROP_HEIGHT, 
        output_folder
        )
