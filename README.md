# Bibliometric Data Classification Tool

This project provides a Python tool for classifying research paper titles and abstracts into academic fields using the Bytez API and DeepSeek model.

## Features
- Classifies each paper into the top 3 most relevant fields with confidence scores (sum = 100%)
- Processes CSV files with `title` and `abstract` columns
- Handles connection errors with automatic retries
- Saves progress after each row (safe for large datasets)

## Requirements
- Python 3.7+
- [bytez](https://pypi.org/project/bytez/) Python package

## Installation
1. Clone this repository or copy the files to your project folder.
2. Install dependencies:
   ```bash
   pip install bytez
   ```

## Usage
1. Prepare your input CSV file (`input.csv`) with at least these columns:
   - `title`
   - `abstract`

2. Run the classifier:
   ```bash
   python classify_main3fields.py
   ```

3. The output will be saved to `output.csv` with columns:
   - `title`, `abstract`, `field_1_na`, `field_1_co`, `field_2_na`, `field_2_co`, `field_3_na`, `field_3_co`

## Error Handling
- If a connection error occurs, the script will retry up to 5 times before marking the row as an error.
- Already processed rows are saved immediately.

## Collaboration
- To contribute, create a new branch, commit your changes, and push to the repository.
- Open a Pull Request for review.

## License
This project is for academic and research use. See LICENSE for details.
