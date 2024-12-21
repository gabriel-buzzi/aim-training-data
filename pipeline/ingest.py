## Ingest data from the generated .csv, remove the start and end of the video while the task was not started and until the record endded
## Save the cleaned data

import pandas as pd
import matplotlib.pyplot as plt
import os
import cv2
from pipeline.src.dataframe import remove_outliers

def ingest(input_folder, output_folder):

    clean_df = remove_outliers(os.path.join(input_folder, 'data.csv'))

    valid_frames = clean_df["Frame"]
    start_frame = valid_frames.min()
    end_frame = valid_frames.max()
    start_idx = valid_frames.idxmin()
    end_idx = valid_frames.idxmax()

    raw_df.iloc[start_idx+1:end_idx].reset_index(drop=True).to_csv(os.path.join(ingested_path, trial, 'ingested.csv'), index=False)

if __name__ == "__main__":

    data_path = os.path.join(
        '/home',
        'gabriel',
        'code',
        'aim-training-data',
        'data'
    )

    raw_path = os.path.join(
        data_path,
        'generated'
    )

    ingested_path = os.path.join(
        data_path,
        'ingested'
    )

    trial = os.listdir(raw_path)[0]

    os.makedirs(os.path.join(ingested_path, trial), exist_ok=True)

    ingest(os.path.join(raw_path, trial), os.path.join(ingested_path, trial))