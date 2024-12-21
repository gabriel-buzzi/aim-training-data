import pandas as pd
import matplotlib.pyplot as plt
import os
import cv2
from pipeline.src.dataframe import remove_outliers
from video import trim_video, hit_miss_red

def ingest(input_folder, output_folder):

    # Ingest data from the generated .csv 
    
    df = pd.read_csv(os.path.join(input_folder, 'data.csv'))
    video = cv2.VideoCapture(os.path.join(input_folder, 'video.mp4'))

    # Remove the start and end of the video while the task was not started and until the record endded
    clean_df = remove_outliers(df)
    
    valid_frames = clean_df["Frame"]
    
    # Save the cleaned data
    start_idx = valid_frames.idxmin()
    end_idx = valid_frames.idxmax()
    df.iloc[start_idx+1:end_idx].reset_index(drop=True).to_csv(os.path.join(
        output_folder,  
        'data.csv'), 
        index=False
        )

    start_frame = valid_frames.min()
    end_frame = valid_frames.max()
    trim_video(
        cap = video, 
        output_path = os.path.join(output_folder, 'video.mp4'), 
        start_frame = start_frame,
        end_frame = end_frame
        )
    
def transform(input_folder, output_folder):
    # Load the cleaned data from ingestion
    df = pd.read_csv(
        os.path.join(
            input_folder,
            'data.csv'
        )
    )

    # Add the columns in the docs
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

    df.to_csv(os.path.join(output_folder, 'data.csv'), index=False)

    video = cv2.VideoCapture(
        os.path.join(
            input_folder,
            'video.mp4'
        )
    )

    hit_miss_red(
        cap = video,
        df = df,
        output_path = os.path.join(output_folder, 'video.mp4')
    )

def serve():
    pass
    