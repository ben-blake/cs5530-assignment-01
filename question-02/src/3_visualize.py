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
FIG_SIZE = (10, 7.5)  # 800x600 at 100 DPI, set DPI=300 when saving
DPI = 300

# Set general matplotlib parameters for cleaner plots
plt.rcParams.update({
    'font.size': 12,                    # Larger base font size
    'axes.titlesize': 16,               # Large title
    'axes.labelsize': 14,               # Clear axis labels
    'xtick.labelsize': 12,              # Readable tick labels
    'ytick.labelsize': 12,
    'legend.fontsize': 12,              # Readable legend
    'axes.spines.top': False,           # Remove top border
    'axes.spines.right': False,         # Remove right border
    'axes.grid': True,                  # Add light grid
    'grid.alpha': 0.3,                  # Make grid subtle
    'figure.figsize': FIG_SIZE,         # Consistent figure size
    'figure.dpi': 100,                  # Screen display DPI
    'savefig.dpi': DPI                  # Higher DPI for saved figures
})

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
    plt.figure()
    
    # Create boxplot with consistent color mapping
    sns.boxplot(x='subject', y='score', hue='gender', data=plot_data, 
               palette={'female': '#e74c3c', 'male': '#3498db'}, linewidth=1.5)
    
    # Calculate and display means
    for subject in ['Math', 'Reading']:
        subject_idx = 0 if subject == 'Math' else 1
        
        # Calculate means for both genders
        male_subset = plot_data[(plot_data['subject'] == subject) & (plot_data['gender'] == 'male')]
        female_subset = plot_data[(plot_data['subject'] == subject) & (plot_data['gender'] == 'female')]
        
        male_mean = male_subset['score'].mean()
        female_mean = female_subset['score'].mean()
        
        # Position text labels
        plt.text(subject_idx - 0.2, female_mean + 3, f'{female_mean:.1f}', 
              ha='center', va='bottom', fontweight='bold', fontsize=12)
        plt.text(subject_idx + 0.2, male_mean + 3, f'{male_mean:.1f}', 
              ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    # Customize plot
    plt.title('Gender Differences: Math vs Reading Scores')
    plt.xlabel('Subject')
    plt.ylabel('Score')
    plt.ylim(0, 100)
    
    # Simplified statistical annotation
    math_male = df[df['gender'] == 'male']['math_score']
    math_female = df[df['gender'] == 'female']['math_score']
    reading_male = df[df['gender'] == 'male']['reading_score']
    reading_female = df[df['gender'] == 'female']['reading_score']
    
    math_ttest = stats.ttest_ind(math_male, math_female)
    reading_ttest = stats.ttest_ind(reading_male, reading_female)
    
    stat_text = f"Math: p={math_ttest.pvalue:.4f} | Reading: p={reading_ttest.pvalue:.4f}"
    plt.annotate(stat_text, xy=(0.5, 0.01), xycoords='figure fraction', 
               ha='center', fontsize=11, bbox=dict(facecolor='white', alpha=0.8))
    
    # Enhance legend
    plt.legend(title=None, loc='upper right')
    
    # Save the figure
    plt.tight_layout()
    plt.savefig(save_path, dpi=DPI, bbox_inches='tight')
    plt.close()
    
    print(f"Saved visualization to {save_path}")


def create_test_prep_impact(df, save_path):
    """B. V2 - Test prep impact on math"""
    
    plt.figure()
    
    # Create simpler boxplots instead of violin plots for clarity
    # Fix the FutureWarning by properly using hue instead of palette directly
    sns.boxplot(x='test_preparation_course', y='math_score', 
              data=df, hue='test_preparation_course', 
              palette=['#2ecc71', '#f39c12'], 
              order=['completed', 'none'], legend=False,
              width=0.6, linewidth=1.5)
    
    # Calculate and display means more clearly
    courses = ['completed', 'none']
    for i, course in enumerate(courses):
        mean_score = df[df['test_preparation_course'] == course]['math_score'].mean()
        plt.text(i, mean_score + 2, f'{mean_score:.1f}', 
              ha='center', va='bottom', fontweight='bold', fontsize=14,
              color='black')
    
    # Add statistical test
    completed = df[df['test_preparation_course'] == 'completed']['math_score']
    none = df[df['test_preparation_course'] == 'none']['math_score']
    ttest_result = stats.ttest_ind(completed, none)
    
    # Customize plot
    plt.title('Impact of Test Preparation on Math Score')
    plt.xlabel('Test Preparation')
    plt.ylabel('Math Score')
    plt.ylim(0, 100)
    
    # Add clearer statistical annotation
    plt.annotate(f"p={ttest_result.pvalue:.4f}", 
               xy=(0.5, 0.01), xycoords='figure fraction', 
               ha='center', fontsize=11, bbox=dict(facecolor='white', alpha=0.8))
    
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
    plt.figure()
    
    # Create grouped bar chart with clearer colors
    bar_colors = ['#3498db', '#2ecc71', '#9b59b6']  # Blue, green, purple
    ax = sns.barplot(x='lunch', y='average_score', hue='subject', data=plot_data, 
                   palette=bar_colors, edgecolor='white', linewidth=1)
    
    # Add simplified value labels on bars
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'{height:.0f}', 
                  (p.get_x() + p.get_width() / 2., height + 0.5), 
                  ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    # Add overall average line for each lunch type
    for i, lunch_type in enumerate(['free/reduced', 'standard']):
        overall_avg = df[df['lunch'] == lunch_type]['overall_avg'].mean()
        plt.axhline(y=overall_avg, xmin=i/2, xmax=(i+1)/2, 
                  color='#e74c3c', linestyle='-', linewidth=2)
        plt.text(i, overall_avg - 3, f'Avg: {overall_avg:.1f}', 
              ha='center', va='top', color='black', fontweight='bold')
    
    # Statistical test
    std_overall = df[df['lunch'] == 'standard']['overall_avg']
    free_overall = df[df['lunch'] == 'free/reduced']['overall_avg']
    ttest_result = stats.ttest_ind(std_overall, free_overall)
    
    # Customize plot
    plt.title('Average Scores by Lunch Type')
    plt.xlabel('Lunch Type')
    plt.ylabel('Score')
    plt.ylim(0, 85)
    
    # Clean up legend
    plt.legend(title=None, loc='upper right', frameon=True, framealpha=0.9)
    
    # Create t-test
    ttest_result = stats.ttest_ind(std_overall, free_overall)

    # Add clearer statistical annotation
    plt.annotate(f"p={ttest_result.pvalue:.4f}", 
               xy=(0.5, 0.01), xycoords='figure fraction', 
               ha='center', fontsize=11,
               bbox=dict(facecolor='white', alpha=0.8))
    
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
    
    # Rename columns/index for display
    pretty_names = {'math_score': 'Math', 'reading_score': 'Reading', 'writing_score': 'Writing'}
    corr_matrix = corr_matrix.rename(index=pretty_names, columns=pretty_names)
    
    # Create the plot with square aspect ratio
    plt.figure(figsize=(8, 6.5))
    
    # Create heatmap with improved readability
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    
    sns.heatmap(
        corr_matrix, 
        annot=True,            # Show the correlation values
        fmt='.2f',             # Simpler number format (2 decimal places)
        cmap=cmap,             # Better color scheme
        mask=mask,             # Show only half of the symmetric matrix
        vmin=0.75, vmax=1.0,   # Focus scale on relevant range
        square=True,           # Make cells square
        linewidths=0.8,        # Thin lines between cells
        annot_kws={"size": 14, "weight": "bold"},  # Make numbers more readable
        cbar_kws={"shrink": .8, "label": "Correlation"}  # Improve colorbar
    )
    
    # Add correlations as text for the upper triangle
    for i in range(len(corr_matrix)):
        for j in range(i+1, len(corr_matrix)):
            plt.text(j+0.5, i+0.5, f'{corr_matrix.iloc[i, j]:.2f}',
                  ha='center', va='center', color='black', fontweight='bold', fontsize=14)
    
    # Customize plot
    plt.title('Subject Score Correlations')
    
    # Save the figure with tight layout
    plt.tight_layout()
    plt.savefig(save_path, dpi=DPI, bbox_inches='tight')
    plt.close()
    
    print(f"Saved visualization to {save_path}")


def create_math_reading_scatter(df, save_path):
    """E. V5 - Math vs reading scatter with trend lines by test prep"""
    
    plt.figure()
    
    # Create scatter plot with clearer colors and better visibility
    groups = df['test_preparation_course'].unique()
    colors = {'completed': '#2ecc71', 'none': '#e67e22'}
    markers = {'completed': 'o', 'none': 'x'}
    
    # Plot each group with regression line
    for group in groups:
        subset = df[df['test_preparation_course'] == group]
        
        # Count observations
        n = len(subset)
        
        # Calculate regression line
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            subset['reading_score'], subset['math_score'])
        
        # Plot scatter with reduced point size and increased clarity
        plt.scatter(subset['reading_score'], subset['math_score'], 
                  alpha=0.5, color=colors[group], s=40,
                  marker=markers[group], edgecolor='none',
                  label=f"{group} (n={n})")
        
        # Add regression line with increased width for visibility
        x = np.array([20, 100])
        y = intercept + slope * x
        plt.plot(x, y, color=colors[group], linewidth=3)
        
        # Add simpler regression equation text
        text_x = 70
        text_y = intercept + slope * text_x + (8 if group == 'completed' else -8)
        plt.text(text_x, text_y, f"R² = {r_value**2:.2f}", 
               color=colors[group], fontweight='bold', fontsize=12, ha='center', 
               bbox=dict(facecolor='white', alpha=0.9, edgecolor=colors[group], boxstyle='round,pad=0.3'))
    
    # Customize plot
    plt.title('Math vs Reading Scores by Test Preparation')
    plt.xlabel('Reading Score')
    plt.ylabel('Math Score')
    plt.xlim(20, 100)
    plt.ylim(20, 100)
    
    # Create legend with clearer labels
    legend = plt.legend(title=None, loc='lower right', 
                      frameon=True, framealpha=0.9, edgecolor='gray')
    
    # Remove reference line - simplify the plot
    
    # Save the figure
    plt.tight_layout()
    plt.savefig(save_path, dpi=DPI, bbox_inches='tight')
    plt.close()
    
    print(f"Saved visualization to {save_path}")


if __name__ == "__main__":
    findings = visualize_data()
    print("\nData visualization complete")
