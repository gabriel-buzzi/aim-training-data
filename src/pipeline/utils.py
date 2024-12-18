def detect_outliers(df, column):
    """
    Detects outliers in a specific column of a DataFrame using the IQR method.
    
    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        column (str): The column name to detect outliers in.

    Returns:
        pd.DataFrame: A DataFrame containing the rows with outliers in the specified column.
        list: Indices of rows identified as outliers.
    """
    Q1 = df[column].quantile(0.25)  # First quartile (25th percentile)
    Q3 = df[column].quantile(0.75)  # Third quartile (75th percentile)
    IQR = Q3 - Q1  # Interquartile range

    # Defining the lower and upper bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Identifying outliers
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    outlier_indices = outliers.index.tolist()

    return outliers, outlier_indices