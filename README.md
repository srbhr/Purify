# Purify

A high-performance text cleaning utility designed for processing large volumes of text data efficiently.

## Features

- Ultra-fast text cleaning using optimized string operations
- Parallel processing for batch text cleaning
- Memory-efficient file processing for handling large files
- Simple API for seamless integration

## Installation

Simply copy the `text_cleaner.py` file to your project directory.

## Usage Examples

### Basic Usage

```python
from text_cleaner import clean_text

# Clean a single text string
text = "Hello, World! This is some sample TEXT; with UPPERCASE letters, and various punctuation marks???"
cleaned_text = clean_text(text)
print(cleaned_text)
# Output: "hello world this is some sample text with uppercase letters and various punctuation marks"
```

### Batch Processing

```python
from text_cleaner import clean_batch

# Clean multiple texts in parallel
texts = [
    "First example with SOME punctuation!!!",
    "Second EXAMPLE with <b>HTML</b> tags.",
    "Third example with numbers 123 and symbols @#$%"
]

# Using default number of workers (CPU count - 1)
cleaned_texts = clean_batch(texts)

# Using a specific number of workers
cleaned_texts = clean_batch(texts, num_workers=4)

for original, cleaned in zip(texts, cleaned_texts):
    print(f"Original: {original}")
    print(f"Cleaned:  {cleaned}")
    print()
```

### File Processing

```python
from text_cleaner import clean_file

# Clean an entire file
input_file = "input.txt"
output_file = "cleaned_output.txt"

# Using default chunk size (100,000 lines)
clean_file(input_file, output_file)

# Using a custom chunk size
clean_file(input_file, output_file, chunk_size=10000)
```

### Integration with Data Processing Pipeline

```python
import pandas as pd
from text_cleaner import clean_batch

# Example with pandas DataFrame
df = pd.read_csv("data.csv")

# Clean the 'text' column
df['cleaned_text'] = clean_batch(df['text'].tolist())

# Save the results
df.to_csv("cleaned_data.csv", index=False)
```

## API Reference

### `clean_text(text)`

Cleans a single text string:

- Converts to lowercase
- Removes all characters except letters, numbers, spaces, and periods
- Normalizes whitespace
- Fixes spacing around periods

Parameters:

- `text` (str): The input text to clean

Returns:

- `str`: The cleaned text

### `clean_batch(texts, num_workers=None)`

Cleans multiple texts in parallel:

- Processes the list of texts using multiple CPU cores
- Uses `concurrent.futures.ProcessPoolExecutor` for parallelization

Parameters:

- `texts` (list): List of strings to clean
- `num_workers` (int, optional): Number of worker processes to use. Defaults to CPU count - 1.

Returns:

- `list`: List of cleaned texts

### `clean_file(input_path, output_path, chunk_size=100000)`

Cleans a file without loading the entire content into memory:

- Processes the file in chunks to manage memory usage
- Writes cleaned text to the output file

Parameters:

- `input_path` (str): Path to the input file
- `output_path` (str): Path where cleaned text will be saved
- `chunk_size` (int, optional): Number of lines to process at once. Default is 100,000.

## Performance Tips

1. For single text cleaning, `clean_text()` is highly optimized and uses pre-compiled regexes for maximum speed.

2. For batch processing:
   - Adjust `num_workers` based on your system's CPU cores and available memory
   - For optimal performance, batch sizes should be a multiple of `num_workers`

3. For file processing:
   - Adjust `chunk_size` based on your available memory
   - Smaller chunks use less memory but have more overhead
   - Larger chunks are more efficient but use more memory

4. When processing very large files (multiple GB):
   - Use `clean_file()` with an appropriate chunk size
   - Consider running on a machine with more CPU cores for faster processing

## License

[Specify your license here]
