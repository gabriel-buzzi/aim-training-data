from pipeline.src.utils import detect_outliers
import pandas as pd

def remove_outliers(df):

    _, x_outliers_idx = detect_outliers(df, 'Center_X')
    _, y_outliers_idx = detect_outliers(df, 'Center_Y')

    outliers_idx = list(set(x_outliers_idx) & set(y_outliers_idx))

    return df.drop(outliers_idx)