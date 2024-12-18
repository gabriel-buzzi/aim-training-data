## Load the cleaned data from ingestion and add the columns in the docs
## Save the transformed data in a new .csv file

import cv2
import pandas as pd
import os

ingested_path = os.path.join(
    '/home',
    'gabriel',
    'code',
    'aim-training-data',
    'data',
    'generated'
)

trial = os.listdir(ingested_path)[0]

# Load the video
video_path = os.path.join(
    ingested_path,
    trial,
    'cropped.mp4'
) 
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    raise IOError("Error opening video file.")

# Count the frames in the video
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Close the video capture object
cap.release()

# Load the DataFrame
df_path = os.path.join(
    ingested_path,
    trial,
    'raw.csv'
)
df = pd.read_csv(df_path)  # Replace with your DataFrame path

# Count the rows in the DataFrame
row_count = len(df)

# Compare the two counts
if frame_count == row_count:
    print(f"The video has the same number of frames ({frame_count}) as the DataFrame has rows ({row_count}).")
else:
    print(f"Mismatch: The video has {frame_count} frames, but the DataFrame has {row_count} rows.")
