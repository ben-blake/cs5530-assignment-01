#!/usr/bin/env python3
"""
Stage 1: Data Ingestion
- Reads the raw student performance data
- Verifies data integrity
- Displays basic information about the dataset
"""

import os
import pandas as pd
import numpy as np

# Define paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
raw_data_path = os.path.join(project_dir, 'data', 'raw', 'StudentsPerformance.csv')

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
    print("\nData preview:")
    print(df.head())
    
    # Check for missing values
    missing = df.isna().sum()
    if missing.sum() > 0:
        print("\nMissing values found:")
        print(missing[missing > 0])
    else:
        print("\nNo missing values found")
    
    # Data types
    print("\nData types:")
    print(df.dtypes)
    
    # Summary statistics for numeric columns
    print("\nNumeric summary statistics:")
    print(df.describe())
    
    # Unique values for categorical columns
    print("\nCategorical columns summary:")
    for col in df.select_dtypes(include=['object']).columns:
        print(f"\n{col} - unique values: {df[col].nunique()}")
        print(df[col].value_counts())
    
    return df

if __name__ == "__main__":
    df = ingest_data()
    print("\nData ingestion complete")
