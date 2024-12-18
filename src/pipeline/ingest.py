## Ingest data from the generated .csv, remove the start and end of the video while the task was not started and until the record endded
## Save the cleaned data

import pandas as pd
import matplotlib.pyplot as plt
import os
from utils import detect_outliers
import cv2

raw_path = os.path.join(
    '/home',
    'gabriel',
    'code',
    'aim-training-data',
    'data',
    'generated'
)

ingested_path = os.path.join(
    '/home',
    'gabriel',
    'code',
    'aim-training-data',
    'data',
    'ingested'
)

trial = os.listdir(raw_path)[0]

os.makedirs(os.path.join(ingested_path, trial), exist_ok=True)

raw_df = pd.read_csv(
    os.path.join(
            raw_path,
            trial,
            'raw.csv'
        )
    )

_, x_outliers_idx = detect_outliers(raw_df, 'Center_X')
_, y_outliers_idx = detect_outliers(raw_df, 'Center_Y')

outliers_idx = list(set(x_outliers_idx) & set(y_outliers_idx))

clean_df = raw_df.drop(outliers_idx)

# Define the range of frames after outlier removal
valid_frames = clean_df["Frame"]
start_frame = valid_frames.min()
end_frame = valid_frames.max()
start_idx = valid_frames.idxmin()
end_idx = valid_frames.idxmax()
print(f"Valid frames: {start_frame} to {end_frame}")

cropped_video_path = os.path.join(
        raw_path,
        trial,
        'cropped.mp4'
    )

trimmed_video_path = os.path.join(
        ingested_path,
        trial,
        'trimmed.mp4'
    )

# Load the original video
cap = cv2.VideoCapture(cropped_video_path)

# Get video properties
fps = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Initialize the video writer for the trimmed video
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(trimmed_video_path, fourcc, fps, (frame_width, frame_height))

# Extract and save frames within the valid range
current_frame = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # Exit at the end of the video

    # Write frames only if they are within the valid range
    if start_frame <= current_frame <= end_frame:
        out.write(frame)

    current_frame += 1
    if current_frame > end_frame:
        break

# Release resources
cap.release()
out.release()
print(f"Trimmed video saved to: {trimmed_video_path}")

raw_df.iloc[start_idx:end_idx].reset_index(drop=True).to_csv(os.path.join(ingested_path, trial, 'ingested.csv'))

outliers_df = raw_df.loc[outliers_idx]

plt.figure()
plt.scatter(x=clean_df['Center_X'], y=clean_df['Center_Y'], s=2)
#plt.scatter(x=outliers_df['Center_X'], y=outliers_df['Center_Y'], s=2)
plt.show()