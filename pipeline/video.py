import cv2
import numpy as np

def trim_video(cap, output_path, start_frame, end_frame):
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Initialize the video writer for the trimmed video
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    # Extract and save frames within the valid range
    current_frame = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # Exit at the end of the video

        # Write frames only if they are within the valid range
        if start_frame < current_frame < end_frame:
            out.write(frame)

        current_frame += 1
        if current_frame >= end_frame:
            break

    # Release resources
    cap.release()
    out.release()

def hit_miss_red(cap, df, output_path):
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    assert len(df) == frame_count, "The number of rows in the dataframe must match the video's frame count."

    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Set up the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    # Iterate through frames and process
    frame_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Check label from the dataframe
        label = df.loc[frame_idx, 'hit']  # Replace 'label' with your column name
        if not label:  # If label is False, tint the frame red
            red_overlay = np.zeros_like(frame)
            red_overlay[:, :, 2] = 100  # Add red color
            frame = cv2.addWeighted(frame, 0.7, red_overlay, 0.3, 0)

        # Write frame to the output video
        out.write(frame)
        frame_idx += 1

    # Release resources
    cap.release()
    out.release()
    #cv2.destroyAllWindows()