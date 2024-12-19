## Load the cleaned data from ingestion and add the columns in the docs
## Save the transformed data in a new .csv file

import cv2
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

ingested_path = os.path.join(
    '/home',
    'gabriel',
    'code',
    'aim-training-data',
    'data',
    'ingested'
)

trial = os.listdir(ingested_path)[0]

transformed_path = os.path.join(
    '/home',
    'gabriel',
    'code',
    'aim-training-data',
    'data',
    'transformed'
)

os.makedirs(os.path.join(transformed_path, trial), exist_ok=True)

# Load the DataFrame
df = pd.read_csv(
    os.path.join(
        ingested_path,
        trial,
        'ingested.csv'
    )
)

FPS = df.iloc[0]['FPS']
CENTER_X = df.iloc[0]['Video_Width']//2
CENTER_Y = df.iloc[0]['Video_Height']//2

def hit_miss(row):
    hit_x = False
    if row['Box_X'] < CENTER_X < row['Box_X']+row['Box_Width']:
        hit_x = True
    hit_y = False
    if row['Box_Y'] < CENTER_Y < row['Box_Y']+row['Box_Width']:
        hit_y = True
    return hit_x and hit_y

df['hit'] = df.apply(hit_miss, axis=1)

df['Center_Speed_X'] = df['Center_X'].diff()
df['Center_Speed_Y'] = df['Center_Y'].diff()

df['Center_Acceleration_X'] = df['Center_Speed_X'].diff()
df['Center_Acceleration_Y'] = df['Center_Speed_Y'].diff()

# Check if the dataframe's frame count matches the video's frame count
cap = cv2.VideoCapture(
    os.path.join(
        ingested_path,
        trial,
        'ingested.mp4'
    )
)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
assert len(df) == frame_count, "The number of rows in the dataframe must match the video's frame count."

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Set up the video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(os.path.join(transformed_path, trial, 'transformed.mp4'), fourcc, fps, (frame_width, frame_height))

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
cv2.destroyAllWindows()

df.to_csv(os.path.join(transformed_path, trial, 'transformed.csv'), index=False)