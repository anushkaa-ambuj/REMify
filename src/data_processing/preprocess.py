import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler

def load_data(file_path):
    """
    Load CSV data into a pandas DataFrame.
    """
    df = pd.read_csv(file_path)
    return df

def handle_missing_values(df):
    """
    Handle missing values in the dataset:
    - Impute missing values with the mean of the previous and next data entry for each column.
    """
    for column in df.columns:
        if df[column].dtype != 'object':  # Only handle numerical columns
            for i in range(1, len(df)-1):
                if pd.isna(df[column].iloc[i]):
                    # Substituting missing value with the mean of the previous and next valid entries
                    df[column].iloc[i] = (df[column].iloc[i-1] + df[column].iloc[i+1]) / 2
    return df

def Standard_scale_data(df, columns_to_scale):
    """
    Standardize the numerical columns (Standard Scaling).
    - Scale the specified columns using Z-score normalization.
    """
    scaler = StandardScaler()
    df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])
    return df

def MinMax_scale_data(df, columns_to_scale):
    """
    Normalize the numerical columns using Min-Max Scaling (to range [0, 1]).
    """
    scaler = MinMaxScaler()
    df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])
    return df

def preprocess_data(file_path):
    """
    Full preprocessing pipeline:
    1. Load data
    2. Handle missing values
    3. Scale data using Min-Max Scaling
    """
    df = load_data(file_path)
    
    # Handle missing values
    df = handle_missing_values(df)

    # Columns that need to be scaled
    numerical_columns = ['RED', 'IR', 'Ax', 'Ay', 'Az', 'Gx', 'Gy', 'Gz', 'Temperature']
    standard_scale_columns = []
    minmax_scale_columns = []

    # Apply Standard Scaling
    df = Standard_scale_data(df, standard_scale_columns)

    # Apply Min-Max Scaling
    df = MinMax_scale_data(df, minmax_scale_columns)

    return df

if __name__ == "__main__":
    # Path to the dataset
    file_path = 'data/raw/sensor_data.csv'

    # Preprocess the data with Min-Max scaling
    processed_data = preprocess_data(file_path)

    # Save the preprocessed data to a new CSV file
    processed_data.to_csv('data/processed/processed_sensor_data.csv', index=False)
    print("Data preprocessing complete! Saved to 'data/processed directory'.")