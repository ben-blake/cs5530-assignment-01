#!/usr/bin/env python3
"""
Stage 1: Data Ingestion
- Reads the raw frailty data
- Verifies data integrity
- Displays basic information about the dataset
"""

import os
import pandas as pd
import numpy as np

# Define paths
raw_data_path = os.path.join('data', 'raw', 'frailty.csv')

# Read the raw data
def ingest_data():
    print("Stage 1: Ingesting Data")
    
    # Check if the data file exists
    if not os.path.exists(raw_data_path):
        raise FileNotFoundError(f"Raw data file not found at {raw_data_path}")
    
    # Load the data
    df = pd.read_csv(raw_data_path)
    
    # Display basic information
    print(f"Loaded {df.shape[0]} records with {df.shape[1]} variables")
    print("Data preview:")
    print(df.head())
    
    # Check for missing values
    missing = df.isna().sum()
    if missing.sum() > 0:
        print("Missing values found:")
        print(missing[missing > 0])
    else:
        print("No missing values found")
    
    # Data types
    print("Data types:")
    print(df.dtypes)
    
    return df

if __name__ == "__main__":
    df = ingest_data()
    print("Data ingestion complete")
