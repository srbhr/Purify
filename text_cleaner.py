import re
import concurrent.futures
import multiprocessing


HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
MULTI_PERIOD_PATTERN = re.compile(r"\.{2,}")
SPACE_PATTERN = re.compile(r"\s+")
SPACE_PERIOD_PATTERN = re.compile(r"\s\.")

ALLOWED_CHARS = set("abcdefghijklmnopqrstuvwxyz0123456789 .")
TRANS_TABLE = {i: None for i in range(128) if chr(i) not in ALLOWED_CHARS}


def clean_text(text):
    """
    Ultra-fast text cleaning: removes unwanted characters, keeps periods, returns lowercase

    Args:
        text (str): Input text to clean

    Returns:
        str: Cleaned text
    """
    text = text.lower()
    text = text.translate(TRANS_TABLE)
    text = SPACE_PATTERN.sub(" ", text)
    text = SPACE_PERIOD_PATTERN.sub(".", text)

    return text.strip()


def clean_batch(texts, num_workers=None):
    """
    Process a batch of texts in parallel for higher throughput

    Args:
        texts (list): List of strings to clean
        num_workers (int, optional): Number of worker processes

    Returns:
        list: Cleaned texts
    """
    if num_workers is None:
        num_workers = max(1, multiprocessing.cpu_count() - 1)

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        return list(executor.map(clean_text, texts))


def clean_file(input_path, output_path, chunk_size=100000):
    """
    Clean a large text file without loading it entirely into memory

    Args:
        input_path (str): Path to input file
        output_path (str): Path where cleaned text will be saved
        chunk_size (int): Number of lines to process at once
    """
    with open(input_path, "r", encoding="utf-8") as infile, open(
        output_path, "w", encoding="utf-8"
    ) as outfile:

        lines_buffer = []
        for line in infile:
            lines_buffer.append(line)

            if len(lines_buffer) >= chunk_size:
                cleaned_lines = clean_batch(lines_buffer)
                outfile.write("\n".join(cleaned_lines) + "\n")
                lines_buffer = []

        if lines_buffer:
            cleaned_lines = clean_batch(lines_buffer)
            outfile.write("\n".join(cleaned_lines))
