#!/usr/bin/env python3
"""
Stage 2: Data Processing
- Handles missing values
- Creates derived variables
- Prepares data for visualization
"""

import os
import pandas as pd
import numpy as np

# Define paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
raw_data_path = os.path.join(project_dir, 'data', 'raw', 'StudentsPerformance.csv')
processed_data_path = os.path.join(project_dir, 'data', 'processed', 'students_processed.csv')

def process_data():
    print("Stage 2: Processing Data")
    
    # Load raw data
    df = pd.read_csv(raw_data_path)
    print(f"Loaded {df.shape[0]} records with {df.shape[1]} variables")
    
    # Clean column names - strip quotes if any and ensure snake_case
    df.columns = [col.strip('"').replace(' ', '_').replace('/', '_') for col in df.columns]
    
    # Check for missing values
    print("\nChecking for missing values...")
    missing = df.isna().sum()
    if missing.sum() > 0:
        print("Missing values found:")
        print(missing[missing > 0])
        
        # Handle missing values (if any)
        for col in df.columns:
            if df[col].isna().sum() > 0:
                if pd.api.types.is_numeric_dtype(df[col]):
                    # Fill numeric columns with median
                    df[col] = df[col].fillna(df[col].median())
                else:
                    # Fill categorical columns with mode
                    df[col] = df[col].fillna(df[col].mode()[0])
    else:
        print("No missing values found")
    
    # Feature engineering
    print("\nEngineering features...")
    
    # Create overall average score
    df['overall_avg'] = (df['math_score'] + df['reading_score'] + df['writing_score']) / 3
    
    # Create performance categories based on overall average
    bins = [0, 40, 60, 75, 100]
    labels = ['Poor', 'Average', 'Good', 'Excellent']
    df['performance_category'] = pd.cut(df['overall_avg'], bins=bins, labels=labels)
    
    # Convert categorical variables to proper category dtype
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        df[col] = df[col].astype('category')
    
    # Save processed data
    os.makedirs(os.path.dirname(processed_data_path), exist_ok=True)
    df.to_csv(processed_data_path, index=False)
    print(f"\nProcessed data saved to {processed_data_path}")
    
    # Display data summary
    print("\nProcessed data preview:")
    print(df.head())
    
    print("\nNew columns added:")
    print(f"- overall_avg: Average of math, reading, and writing scores")
    print(f"- performance_category: Performance level based on overall average")
    
    return df

if __name__ == "__main__":
    processed_df = process_data()
    print("\nData processing complete")
