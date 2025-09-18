#!/usr/bin/env python3
"""
Stage 2: Data Processing
- Standardizes units (inches to meters, pounds to kilograms)
- Engineers features (BMI, Age Groups)
- Encodes categorical variables
"""

import os
import pandas as pd
import numpy as np

# Define paths
raw_data_path = os.path.join('data', 'raw', 'frailty.csv')
processed_data_path = os.path.join('data', 'processed', 'frailty_processed.csv')

def process_data():
    print("Stage 2: Processing Data")
    
    # Load raw data
    df = pd.read_csv(raw_data_path)
    print(f"Loaded {df.shape[0]} records with {df.shape[1]} variables")

    # Rename grip strength to Grip_kg
    df.rename(columns={'Grip strength': 'Grip_kg'}, inplace=True)
    
    # Unit standardization
    print("Standardizing units...")
    df['Height_m'] = df['Height'] * 0.0254  # Convert inches to meters
    df['Weight_kg'] = df['Weight'] * 0.45359237  # Convert pounds to kilograms
    
    # Feature engineering
    print("Engineering features...")
    # Calculate BMI (rounded to 2 decimal places)
    df['BMI'] = round(df['Weight_kg'] / (df['Height_m'] ** 2), 2)
    
    # Create AgeGroup categorical variable
    conditions = [
        (df['Age'] < 30),
        (df['Age'] >= 30) & (df['Age'] <= 45),
        (df['Age'] > 45) & (df['Age'] <= 60),
        (df['Age'] > 60)
    ]
    choices = ['<30', '30-45', '46-60', '>60']
    df['AgeGroup'] = np.select(conditions, choices, default='Unknown')
    
    # Categorical encoding
    print("Encoding categorical variables...")
    # Binary encoding for Frailty (Y→1, N→0)
    df['Frailty_binary'] = (df['Frailty'] == 'Y').astype('int8')
    
    # One-hot encoding for AgeGroup
    age_group_dummies = pd.get_dummies(df['AgeGroup'], prefix='AgeGroup')
    # Convert boolean True/False to binary 1/0
    age_group_dummies = age_group_dummies.astype('int8')
    df = pd.concat([df, age_group_dummies], axis=1)
    
    # Rename columns to match requirements
    df.rename(columns={
        'AgeGroup_<30': 'AgeGroup_<30',
        'AgeGroup_30-45': 'AgeGroup_30–45',
        'AgeGroup_46-60': 'AgeGroup_46–60',
        'AgeGroup_>60': 'AgeGroup_>60'
    }, inplace=True)
    
    # Save processed data
    os.makedirs(os.path.dirname(processed_data_path), exist_ok=True)
    df.to_csv(processed_data_path, index=False)
    print(f"Processed data saved to {processed_data_path}")
    
    # Display data preview
    print("Processed data preview:")
    print(df.head())
    
    return df

if __name__ == "__main__":
    processed_df = process_data()
    print("Data processing complete")
