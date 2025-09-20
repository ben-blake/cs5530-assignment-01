# CS5530 Assignment 1

Ben Blake \<bebpph@umsystem.edu\>

## Question 1 - Frailty Data Analysis

### Description

Implement a three-stage data workflow (ingest → process → analyze) for analyzing frailty data from 10 female participants.

Findings are located in `question-01/reports/findings.md`.

### Structure

```
question-01/
├── data/
│   ├── raw/            # Original, unmodified data
│   └── processed/      # Transformed and cleaned data
├── src/                # Source code
│   ├── 1_ingest.py     # Stage 1: Data ingestion
│   ├── 2_process.py    # Stage 2: Data processing
│   ├── 3_analyze.py    # Stage 3: Data analysis
│   └── run_workflow.py # Main script to run the entire workflow
├── reports/            # Analysis outputs and reports
|   └── findings.md     # Analysis findings
└── README.md           # Project documentation
```

### Workflow Stages

#### Stage 1: Data Ingestion

- Read raw data from CSV
- Verify data integrity
- Basic data exploration

#### Stage 2: Data Processing

- Unit standardization (inches to meters, pounds to kilograms)
- Feature engineering (BMI calculation, age grouping)
- Categorical variable encoding (binary, one-hot encoding)

#### Stage 3: Data Analysis

- Compute summary statistics
- Analyze relationship between grip strength and frailty
- Generate reports with findings

## Question 2 - Student Performance Data Visualization

### Description

Implement a three-stage data workflow (ingest → process → visualize) for analyzing student performance data, with five distinct visualization tasks.

Visualizations and interpretions are located in `question-02/reports/`.

### Structure

```
question-02/
├── data/
│   ├── raw/            # Original, unmodified data
│   └── processed/      # Transformed and cleaned data
├── src/                # Source code
│   ├── 1_ingest.py     # Stage 1: Data ingestion
│   ├── 2_process.py    # Stage 2: Data processing
│   ├── 3_visualize.py  # Stage 3: Data visualization
│   └── run_workflow.py # Main script to run the entire workflow
├── reports/            # Visualizations and findings
│   ├── V1_gender_boxplots.png
│   ├── V2_test_prep_math.png
│   ├── V3_lunch_performance.png
│   ├── V4_subject_correlations.png
│   ├── V5_math_reading_scatter.png
│   └── visualization_findings.md
└── README.md           # Project documentation
```

### Workflow Stages

#### Stage 1: Data Ingestion

- Read raw data from CSV
- Verify data integrity
- Basic data exploration

#### Stage 2: Data Processing

- Clean column names
- Handle missing values (if any)
- Feature engineering (overall average score, performance categories)

#### Stage 3: Data Visualization

The visualization stage creates five distinct visualizations:

1. **V1: Gender boxplots (math vs reading)**  
   Side-by-side boxplots analyzing gender differences in math and reading scores.

2. **V2: Test prep impact on math**  
   Violin plots showing how test preparation affects math scores.

3. **V3: Lunch type and average performance**  
   Grouped bar chart examining the relationship between lunch type and subject performance.

4. **V4: Subject correlations**  
   Correlation heatmap showing the strength of relationships between math, reading, and writing scores.

5. **V5: Math vs reading with trend lines by test prep**  
   Scatter plot with regression lines analyzing the math-reading score relationship by test preparation status.

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run Question 1 workflow
python question-01/src/run_workflow.py

# Run Question 2 workflow
python question-02/src/run_workflow.py
```
