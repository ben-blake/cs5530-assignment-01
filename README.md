# CS5530 Assignment 1

Ben Blake \<bebpph@umsystem.edu\>

## Question 1

### Description

Implement a three-stage data workflow (ingest → process → analyze) for analyzing frailty data from 10 female participants.

Findings are located in `question-01/reports/findings.md`.

## Structure

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

## Workflow Stages

### Stage 1: Data Ingestion

- Read raw data from CSV
- Verify data integrity
- Basic data exploration

### Stage 2: Data Processing

- Unit standardization (inches to meters, pounds to kilograms)
- Feature engineering (BMI calculation, age grouping)
- Categorical variable encoding (binary, one-hot encoding)

### Stage 3: Data Analysis

- Compute summary statistics
- Analyze relationship between grip strength and frailty
- Generate reports with findings

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the complete workflow
python question-01/src/run_workflow.py
```
