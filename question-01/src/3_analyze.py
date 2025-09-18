#!/usr/bin/env python3
"""
Stage 3: Data Analysis
- Computes summary statistics for numeric columns
- Calculates correlation between Grip_kg and Frailty_binary
- Generates reports with findings
"""

import os
import pandas as pd
import numpy as np
from scipy import stats

# Define paths
processed_data_path = os.path.join('data', 'processed', 'frailty_processed.csv')
findings_path = os.path.join('reports', 'findings.md')

def analyze_data():
    print("Stage 3: Analyzing Data")
    
    # Load processed data
    df = pd.read_csv(processed_data_path)
    print(f"Loaded {df.shape[0]} records with {df.shape[1]} variables")
    
    # Select numeric columns for summary statistics
    numeric_cols = ['Height', 'Weight', 'Height_m', 'Weight_kg', 'BMI', 'Age', 'Grip_kg']
    
    # Compute summary statistics
    print("Computing summary statistics...")
    summary = df[numeric_cols].describe().T
    
    # Compute median separately (not included in describe())
    summary['median'] = df[numeric_cols].median()
    
    # Rearrange columns for better readability
    summary = summary[['mean', 'median', 'std']]
    
    # Calculate correlation between Grip_kg and Frailty_binary
    print("Calculating correlations...")
    correlation = df['Grip_kg'].corr(df['Frailty_binary'])
    
    # Generate findings report
    print("Generating findings report...")
    os.makedirs(os.path.dirname(findings_path), exist_ok=True)
    
    with open(findings_path, 'w') as f:
        f.write("# Frailty Data Analysis Findings\n\n")
        
        f.write("## Summary Statistics for Numeric Variables\n\n")
        f.write(summary.to_markdown(floatfmt=".2f"))
        f.write("\n\n")
        
        f.write("## Relationship between Grip Strength and Frailty\n\n")
        f.write(f"Correlation between Grip_kg and Frailty_binary: {correlation:.4f}\n\n")
        
        if correlation < 0:
            f.write("The negative correlation indicates that **higher** grip strength is associated with **lower** frailty (Frailty_binary=0 means N).\n")
            f.write("This supports the hypothesis that reduced grip strength correlates with higher frailty scores.\n\n")
        elif correlation > 0:
            f.write("The positive correlation indicates that **higher** grip strength is associated with **higher** frailty (Frailty_binary=1 means Y).\n")
            f.write("This contradicts the expected hypothesis that reduced grip strength correlates with higher frailty scores.\n\n")
        else:
            f.write("No correlation was found between grip strength and frailty.\n\n")
    
    print(f"Findings saved to {findings_path}")
    return summary, correlation

if __name__ == "__main__":
    summary, correlation = analyze_data()
    print(f"Data analysis complete. Correlation between Grip_kg and Frailty_binary: {correlation:.4f}")
