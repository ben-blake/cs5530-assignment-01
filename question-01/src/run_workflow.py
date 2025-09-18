#!/usr/bin/env python3
"""
Main workflow runner
- Executes all three stages of the frailty data analysis workflow
- Ingest → Process → Analyze
"""

import os
import sys
import time
import importlib.util
import sys

# Dynamically import the modules
def import_module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Import our workflow modules
ingest_module = import_module_from_file("ingest", "src/1_ingest.py")
process_module = import_module_from_file("process", "src/2_process.py")
analyze_module = import_module_from_file("analyze", "src/3_analyze.py")

# Get the functions
ingest_data = ingest_module.ingest_data
process_data = process_module.process_data
analyze_data = analyze_module.analyze_data

def run_workflow():
    """Run the complete three-stage workflow."""
    print("="*50)
    print("STARTING FRAILTY DATA ANALYSIS WORKFLOW")
    print("="*50)
    
    # Stage 1: Ingest
    print("\n" + "="*50)
    print("STAGE 1: DATA INGESTION")
    print("="*50)
    start_time = time.time()
    ingest_data()
    print(f"Completed in {time.time() - start_time:.2f} seconds")
    
    # Stage 2: Process
    print("\n" + "="*50)
    print("STAGE 2: DATA PROCESSING")
    print("="*50)
    start_time = time.time()
    process_data()
    print(f"Completed in {time.time() - start_time:.2f} seconds")
    
    # Stage 3: Analyze
    print("\n" + "="*50)
    print("STAGE 3: DATA ANALYSIS")
    print("="*50)
    start_time = time.time()
    summary, correlation = analyze_data()
    print(f"Completed in {time.time() - start_time:.2f} seconds")
    
    # Report completion
    print("\n" + "="*50)
    print("WORKFLOW COMPLETED SUCCESSFULLY")
    print("="*50)
    print(f"Results saved to reports/findings.md")
    print(f"Correlation between Grip strength and Frailty: {correlation:.4f}")
    
    return True

if __name__ == "__main__":
    run_workflow()
