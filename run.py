#!/usr/bin/env python3
"""
Simple benchmarking script for the text cleaner.
Tests performance on specified input file.
"""

import time
import gc
import sys
import os

# Import optimized cleaner
from text_cleaner import clean_text, clean_batch, clean_file

#=============================================================================
# CONFIGURATION - Edit these values to customize the benchmark
#=============================================================================
# Input file to test (path to file)
INPUT_FILE = "100mb_file.txt"

# Output file where cleaned text will be saved
OUTPUT_FILE = "cleaned_output.txt"

# Chunk sizes to test for file processing (in lines)
CHUNK_SIZES = [100000, 1000000, 10000000]  # 10K, 100K, 1MB

# Worker counts to test for batch processing
WORKER_COUNTS = [None, 2, 4, 8]  # None = auto (CPU count - 1)
#=============================================================================

def benchmark(name, func, data):
    """Run a simple benchmark and print the results"""
    print(f"\nTesting {name}...")
    
    # Force garbage collection before timing
    gc.collect()
    
    # Measure execution time
    start_time = time.time()
    result = func(data)
    end_time = time.time()
    
    execution_time = end_time - start_time
    print(f"  Time: {execution_time:.6f} seconds")
    print(f"  Processing speed: {len(data) / execution_time / 1024 / 1024:.2f} MB/second")
    
    return execution_time, result

def main():
    print("TEXT CLEANER BENCHMARK")
    print("=====================")
    print(f"Input file: {INPUT_FILE}")
    print(f"Output file: {OUTPUT_FILE}")
    
    try:
        # Check if input file exists
        if not os.path.exists(INPUT_FILE):
            print(f"Error: {INPUT_FILE} not found in the current directory.")
            return
            
        # Get file size
        file_size = os.path.getsize(INPUT_FILE)
        file_size_mb = file_size / (1024 * 1024)
        print(f"Found {INPUT_FILE} ({file_size_mb:.2f} MB)")
        
        # Test 1: Single text processing
        print("\n--- SINGLE TEXT PROCESSING ---")
        
        # Load a sample of text
        with open(INPUT_FILE, "r", encoding="utf-8", errors="replace") as f:
            sample = f.read(100000)  # First 100K characters
        
        sample_size_kb = len(sample) / 1024
        print(f"Testing with {sample_size_kb:.2f} KB sample")
        
        # Test the clean_text function
        time1, result1 = benchmark("clean_text", clean_text, sample)
        
        # Output sample of cleaned text
        print("\nSample of cleaned text (first 100 chars):")
        print(result1[:100])
        
        # Test 2: Full file processing
        print("\n--- FULL FILE PROCESSING ---")
        print("Processing entire file with clean_file function...")
        
        # Benchmark different chunk sizes
        for chunk_size in CHUNK_SIZES:
            # Force garbage collection
            gc.collect()
            
            # Time the operation
            print(f"\nTesting with chunk_size={chunk_size}")
            start_time = time.time()
            clean_file(INPUT_FILE, OUTPUT_FILE, chunk_size)
            end_time = time.time()
            
            # Calculate performance
            execution_time = end_time - start_time
            processing_speed = file_size / execution_time / 1024 / 1024  # MB/second
            
            print(f"  Time: {execution_time:.6f} seconds")
            print(f"  Processing speed: {processing_speed:.2f} MB/second")
        
        # Get output file size
        if os.path.exists(OUTPUT_FILE):
            cleaned_size = os.path.getsize(OUTPUT_FILE)
            reduction = (1 - (cleaned_size / file_size)) * 100
            print(f"\nOutput file size: {cleaned_size / 1024 / 1024:.2f} MB")
            print(f"Size reduction: {reduction:.2f}%")
        
        # Test 3: Batch processing
        print("\n--- BATCH PROCESSING ---")
        
        # Read a batch of lines for testing
        with open(INPUT_FILE, "r", encoding="utf-8", errors="replace") as f:
            # Try to read 10,000 lines, but handle EOF gracefully
            lines = []
            for _ in range(10000):
                line = f.readline()
                if not line:
                    break
                lines.append(line)
        
        print(f"Testing batch processing with {len(lines)} lines")
        
        # Test different worker counts
        for workers in WORKER_COUNTS:
            # Force garbage collection
            gc.collect()
            
            # Time the operation
            print(f"\nTesting with workers={workers if workers else 'auto'}")
            start_time = time.time()
            clean_batch(lines, num_workers=workers)
            end_time = time.time()
            
            # Calculate performance
            execution_time = end_time - start_time
            lines_per_second = len(lines) / execution_time
            
            print(f"  Time: {execution_time:.6f} seconds")
            print(f"  Speed: {lines_per_second:.2f} lines/second")
        
        print("\nBenchmark complete!")
        print(f"Cleaned file saved as: {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()