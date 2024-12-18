import cv2

# Input video
video_path = "task.mp4"
output_path = "cropped_task.mp4"  # Path to save the cropped video

# Open the video file
cap = cv2.VideoCapture(video_path)

# Check if the video file opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Get original video dimensions
original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Define the crop dimensions (adjustable)
crop_width = 300  # Desired width of the cropped video
crop_height = 300  # Desired height of the cropped video

# Calculate cropping coordinates (center of the screen)
start_x = (original_width - crop_width) // 2
start_y = (original_height - crop_height) // 2
end_x = start_x + crop_width
end_y = start_y + crop_height

# Define the codec and create VideoWriter to save the cropped video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 files
out = cv2.VideoWriter(output_path, fourcc, fps, (crop_width, crop_height))

# Loop through video frames
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("End of the video.")
        break

    # Crop the frame to the center
    cropped_frame = frame[start_y:end_y, start_x:end_x]

    # Write the cropped frame to the output video
    out.write(cropped_frame)

    # Display the cropped frame (optional)
    cv2.imshow("Cropped Video", cropped_frame)

    # Press 'q' to exit early
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
print(f"Cropped video saved to {output_path}")
