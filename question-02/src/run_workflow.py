#!/usr/bin/env python3
"""
Main workflow runner
- Executes all three stages of the student performance data analysis workflow
- Ingest → Process → Visualize
"""

import os
import sys
import time
import importlib.util

# Dynamically import the modules
def import_module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Get the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Import our workflow modules
ingest_module = import_module_from_file("ingest", os.path.join(script_dir, "1_ingest.py"))
process_module = import_module_from_file("process", os.path.join(script_dir, "2_process.py"))
visualize_module = import_module_from_file("visualize", os.path.join(script_dir, "3_visualize.py"))

# Get the functions
ingest_data = ingest_module.ingest_data
process_data = process_module.process_data
visualize_data = visualize_module.visualize_data

def run_workflow():
    """Run the complete three-stage workflow."""
    print("="*50)
    print("STARTING STUDENT PERFORMANCE DATA ANALYSIS WORKFLOW")
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
    
    # Stage 3: Visualize
    print("\n" + "="*50)
    print("STAGE 3: DATA VISUALIZATION")
    print("="*50)
    start_time = time.time()
    findings = visualize_data()
    print(f"Completed in {time.time() - start_time:.2f} seconds")
    
    # Report completion
    print("\n" + "="*50)
    print("WORKFLOW COMPLETED SUCCESSFULLY")
    print("="*50)
    print(f"Visualizations saved to the reports directory")
    print(f"Created 5 visualizations")
    
    return True

if __name__ == "__main__":
    run_workflow()
