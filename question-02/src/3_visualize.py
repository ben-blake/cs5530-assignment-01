#!/usr/bin/env python3
"""
Stage 3: Data Visualization
- Creates 5 visualization tasks:
  A. Gender boxplots (math vs reading)
  B. Test prep impact on math
  C. Lunch type and average performance
  D. Subject correlations heatmap
  E. Math vs reading scatter with trend lines by test prep
- Generates reports with findings
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator
from scipy import stats

# Set the style for all plots
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("talk")

# Define paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
processed_data_path = os.path.join(project_dir, 'data', 'processed', 'students_processed.csv')
reports_path = os.path.join(project_dir, 'reports')
findings_path = os.path.join(reports_path, 'visualization_findings.md')

# Common figure parameters
FIG_SIZE = (10, 7.5)  # 800x600 at 100 DPI, we'll set DPI=300 when saving
DPI = 300

def visualize_data():
    print("Stage 3: Data Visualization")
    
    # Load processed data
    df = pd.read_csv(processed_data_path)
    print(f"Loaded {df.shape[0]} records with {df.shape[1]} variables")
    
    # Create reports directory if it doesn't exist
    os.makedirs(reports_path, exist_ok=True)
    
    # A. V1 - Gender boxplots (math vs reading)
    print("\nCreating Visualization 1: Gender boxplots")
    v1_path = os.path.join(reports_path, 'V1_gender_boxplots.png')
    create_gender_boxplots(df, v1_path)
    
    # B. V2 - Test prep impact on math
    print("Creating Visualization 2: Test prep impact on math")
    v2_path = os.path.join(reports_path, 'V2_test_prep_math.png')
    create_test_prep_impact(df, v2_path)
    
    # C. V3 - Lunch type and average performance
    print("Creating Visualization 3: Lunch type and performance")
    v3_path = os.path.join(reports_path, 'V3_lunch_performance.png')
    create_lunch_performance(df, v3_path)
    
    # D. V4 - Subject correlations
    print("Creating Visualization 4: Subject correlations")
    v4_path = os.path.join(reports_path, 'V4_subject_correlations.png')
    create_subject_correlations(df, v4_path)
    
    # E. V5 - Math vs reading with trend lines by test prep
    print("Creating Visualization 5: Math vs reading scatter")
    v5_path = os.path.join(reports_path, 'V5_math_reading_scatter.png')
    create_math_reading_scatter(df, v5_path)
    
    print("\nAll visualizations created successfully")
    return True


def create_gender_boxplots(df, save_path):
    """A. V1 - Gender boxplots (math vs reading)"""
    
    # Prepare data for plotting
    math_by_gender = df[['gender', 'math_score']].copy()
    math_by_gender['subject'] = 'Math'
    math_by_gender.rename(columns={'math_score': 'score'}, inplace=True)
    
    reading_by_gender = df[['gender', 'reading_score']].copy()
    reading_by_gender['subject'] = 'Reading'
    reading_by_gender.rename(columns={'reading_score': 'score'}, inplace=True)
    
    plot_data = pd.concat([math_by_gender, reading_by_gender])
    
    # Create the plot
    plt.figure(figsize=FIG_SIZE)
    
    # Create boxplot
    sns.boxplot(x='subject', y='score', hue='gender', data=plot_data, palette='viridis')
    
    # Calculate and display means
    for subject in ['Math', 'Reading']:
        for gender in ['male', 'female']:
            subset = plot_data[(plot_data['subject'] == subject) & (plot_data['gender'] == gender)]
            mean_score = subset['score'].mean()
            plt.scatter(x=0 if subject == 'Math' else 1, y=mean_score, 
                     marker='o', color='black', s=80, zorder=3)
            plt.text(0 if subject == 'Math' else 1, mean_score + 2, 
                  f'Mean: {mean_score:.1f}', 
                  ha='center', va='bottom', fontweight='bold')
    
    # Customize plot
    plt.title('Math vs Reading Score Distribution by Gender', fontsize=16)
    plt.xlabel('Subject', fontsize=14)
    plt.ylabel('Score (0-100)', fontsize=14)
    plt.ylim(0, 100)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add statistical annotation
    math_male = df[df['gender'] == 'male']['math_score']
    math_female = df[df['gender'] == 'female']['math_score']
    reading_male = df[df['gender'] == 'male']['reading_score']
    reading_female = df[df['gender'] == 'female']['reading_score']
    
    math_ttest = stats.ttest_ind(math_male, math_female)
    reading_ttest = stats.ttest_ind(reading_male, reading_female)
    
    plt.figtext(0.5, 0.01, 
              f"Math t-test: p={math_ttest.pvalue:.4f} | Reading t-test: p={reading_ttest.pvalue:.4f}", 
              ha='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    
    # Save the figure
    plt.tight_layout()
    plt.savefig(save_path, dpi=DPI, bbox_inches='tight')
    plt.close()
    
    print(f"Saved visualization to {save_path}")


def create_test_prep_impact(df, save_path):
    """B. V2 - Test prep impact on math"""
    
    plt.figure(figsize=FIG_SIZE)
    
    # Create violin plots with embedded boxplots - reverse the order with order parameter
    sns.violinplot(x='test_preparation_course', y='math_score', 
                 data=df, palette='viridis', inner='box', order=['completed', 'none'])
    
    # Add individual data points with jitter
    sns.stripplot(x='test_preparation_course', y='math_score', 
                data=df, color='black', alpha=0.3, size=3, jitter=True, order=['completed', 'none'])
    
    # Calculate and display means - note the index is reversed
    courses = ['completed', 'none']
    for i, course in enumerate(courses):
        mean_score = df[df['test_preparation_course'] == course]['math_score'].mean()
        plt.scatter(x=i, y=mean_score, marker='o', color='red', s=100, zorder=3)
        plt.text(i, mean_score + 2, f'Mean: {mean_score:.1f}', 
              ha='center', va='bottom', fontweight='bold', color='red')
    
    # Add statistical test
    completed = df[df['test_preparation_course'] == 'completed']['math_score']
    none = df[df['test_preparation_course'] == 'none']['math_score']
    ttest_result = stats.ttest_ind(completed, none)
    
    # Customize plot
    plt.title('Impact of Test Preparation on Math Score', fontsize=16)
    plt.xlabel('Test Preparation Course', fontsize=14)
    plt.ylabel('Math Score (0-100)', fontsize=14)
    plt.ylim(0, 100)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add statistical annotation
    plt.figtext(0.5, 0.01, 
              f"t-test: p={ttest_result.pvalue:.4f}", 
              ha='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    
    # Save the figure
    plt.tight_layout()
    plt.savefig(save_path, dpi=DPI, bbox_inches='tight')
    plt.close()
    
    print(f"Saved visualization to {save_path}")


def create_lunch_performance(df, save_path):
    """C. V3 - Lunch type and average performance"""
    
    # Prepare data for plotting
    subjects = ['math_score', 'reading_score', 'writing_score']
    means = df.groupby('lunch')[subjects].mean().reset_index()
    
    # Reshape for grouped bar chart
    plot_data = pd.melt(means, id_vars='lunch', value_vars=subjects,
                       var_name='subject', value_name='average_score')
    
    # Rename for better display
    plot_data['subject'] = plot_data['subject'].str.replace('_score', '').str.capitalize()
    
    # Create the plot
    plt.figure(figsize=FIG_SIZE)
    
    # Create grouped bar chart
    ax = sns.barplot(x='lunch', y='average_score', hue='subject', data=plot_data, palette='viridis')
    
    # Add value labels on bars
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}', 
                  (p.get_x() + p.get_width() / 2., p.get_height()), 
                  ha='center', va='bottom', fontweight='bold')
    
    # Add overall average line for each lunch type
    for i, lunch_type in enumerate(['free/reduced', 'standard']):
        overall_avg = df[df['lunch'] == lunch_type]['overall_avg'].mean()
        plt.axhline(y=overall_avg, xmin=i/2, xmax=(i+1)/2, 
                  color='red', linestyle='--', linewidth=2)
        plt.text(i, overall_avg - 4, f'Overall: {overall_avg:.1f}', 
              ha='center', va='top', color='red', fontweight='bold')
    
    # Statistical test
    std_overall = df[df['lunch'] == 'standard']['overall_avg']
    free_overall = df[df['lunch'] == 'free/reduced']['overall_avg']
    ttest_result = stats.ttest_ind(std_overall, free_overall)
    
    # Customize plot
    plt.title('Average Test Scores by Lunch Type', fontsize=16)
    plt.xlabel('Lunch Type', fontsize=14)
    plt.ylabel('Average Score (0-100)', fontsize=14)
    plt.ylim(0, 100)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Subject')
    
    # Add statistical annotation
    plt.figtext(0.5, 0.01, 
              f"Overall average t-test: p={ttest_result.pvalue:.4f}", 
              ha='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    
    # Save the figure
    plt.tight_layout()
    plt.savefig(save_path, dpi=DPI, bbox_inches='tight')
    plt.close()
    
    print(f"Saved visualization to {save_path}")


def create_subject_correlations(df, save_path):
    """D. V4 - Subject correlations heatmap"""
    
    # Prepare data for correlation analysis
    subjects = ['math_score', 'reading_score', 'writing_score']
    corr_matrix = df[subjects].corr()
    
    # Create the plot
    plt.figure(figsize=FIG_SIZE)
    
    # Create heatmap
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='viridis', 
             mask=mask, vmin=0, vmax=1, square=True, linewidths=1, cbar_kws={"shrink": .8})
    
    # Add correlations as text for the masked upper triangle
    for i in range(len(corr_matrix)):
        for j in range(i+1, len(corr_matrix)):
            plt.text(j+0.5, i+0.5, f'{corr_matrix.iloc[i, j]:.3f}',
                  ha='center', va='center', color='black', fontweight='bold')
    
    # Customize plot
    plt.title('Correlation Heatmap Between Subject Scores', fontsize=16)
    plt.tight_layout()
    plt.savefig(save_path, dpi=DPI, bbox_inches='tight')
    plt.close()
    
    print(f"Saved visualization to {save_path}")


def create_math_reading_scatter(df, save_path):
    """E. V5 - Math vs reading scatter with trend lines by test prep"""
    
    plt.figure(figsize=FIG_SIZE)
    
    # Create scatter plot with different colors for test prep groups
    groups = df['test_preparation_course'].unique()
    colors = {'completed': 'green', 'none': 'orange'}
    
    # Plot each group with regression line
    for group in groups:
        subset = df[df['test_preparation_course'] == group]
        
        # Count observations
        n = len(subset)
        
        # Calculate regression line
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            subset['reading_score'], subset['math_score'])
        
        # Plot scatter
        plt.scatter(subset['reading_score'], subset['math_score'], 
                  alpha=0.6, color=colors[group], 
                  label=f"{group} (n={n})")
        
        # Add regression line
        x = np.array([0, 100])
        y = intercept + slope * x
        plt.plot(x, y, color=colors[group], linewidth=2)
        
        # Add regression equation text
        text_x = subset['reading_score'].mean()
        text_y = intercept + slope * text_x + 5
        plt.text(text_x, text_y, f"y = {intercept:.1f} + {slope:.2f}x\nR² = {r_value**2:.2f}", 
               color=colors[group], fontweight='bold', ha='center', bbox=dict(facecolor='white', alpha=0.7))
    
    # Customize plot
    plt.title('Math vs Reading Scores by Test Preparation Status', fontsize=16)
    plt.xlabel('Reading Score', fontsize=14)
    plt.ylabel('Math Score', fontsize=14)
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.grid(linestyle='--', alpha=0.7)
    plt.legend(title='Test Preparation')
    
    # Add reference line (y=x)
    plt.plot([0, 100], [0, 100], color='gray', linestyle='--', alpha=0.5)
    
    # Save the figure
    plt.tight_layout()
    plt.savefig(save_path, dpi=DPI, bbox_inches='tight')
    plt.close()
    
    print(f"Saved visualization to {save_path}")


if __name__ == "__main__":
    findings = visualize_data()
    print("\nData visualization complete")
