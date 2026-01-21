"""
Batch classification of papers from CSV file
Input: CSV with 'title' and 'abstract' columns
Output: CSV with title, abstract, and 6 field columns
"""

import os
import sys
import csv
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from tqdm import tqdm
from datetime import datetime

# Load environment variables
root_dir = Path(__file__).parent.parent.parent
env_path = root_dir / '.env'
load_dotenv(env_path)

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from services.llm_field_classifier import LLMFieldClassifier


def process_csv(input_file: str, output_file: str = None):
    """
    Process a CSV file and classify all papers
    
    Args:
        input_file: Path to input CSV with 'title' and 'abstract' columns
        output_file: Path to output CSV (optional, auto-generated if not provided)
    """
    
    # Validate input file
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file not found: {input_file}")
        return
    
    # Generate output filename if not provided
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"classified_papers_{timestamp}.csv"
    
    print("=" * 70)
    print("BATCH PAPER CLASSIFICATION")
    print("=" * 70)
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    print()
    
    # Read input CSV
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return
    
    # Validate required columns
    if 'title' not in df.columns or 'abstract' not in df.columns:
        print("❌ Error: CSV must contain 'title' and 'abstract' columns")
        print(f"Found columns: {list(df.columns)}")
        return
    
    print(f"✅ Loaded {len(df)} papers from CSV")
    print()
    
    # Initialize classifier
    print("Initializing LLM classifier...")
    classifier = LLMFieldClassifier(
        provider="openrouter",
        model="openai/gpt-4o-mini",
        cache_enabled=True
    )
    print("✅ Classifier ready")
    print()
    
    # Prepare output columns
    output_rows = []
    
    # Process each paper
    print("Processing papers...")
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Classifying"):
        title = str(row['title'])
        abstract = str(row['abstract'])
        
        # Skip if title or abstract is empty
        if pd.isna(row['title']) or pd.isna(row['abstract']) or not title or not abstract:
            print(f"\n⚠️  Skipping row {idx + 1}: Missing title or abstract")
            # Add empty fields
            output_rows.append({
                'title': title,
                'abstract': abstract,
                'field_1_code': '',
                'field_1_name': '',
                'field_1_confidence': '',
                'field_2_code': '',
                'field_2_name': '',
                'field_2_confidence': '',
                'field_3_code': '',
                'field_3_name': '',
                'field_3_confidence': '',
                'field_4_code': '',
                'field_4_name': '',
                'field_4_confidence': '',
                'field_5_code': '',
                'field_5_name': '',
                'field_5_confidence': '',
                'field_6_code': '',
                'field_6_name': '',
                'field_6_confidence': ''
            })
            continue
        
        try:
            # Classify the paper
            result = classifier.classify(
                title=title,
                abstract=abstract,
                return_names=True
            )
            
            # Prepare output row
            output_row = {
                'title': title,
                'abstract': abstract
            }
            
            # Add 6 fields with code, name, and confidence
            for i, field in enumerate(result['fields'][:6], 1):
                output_row[f'field_{i}_code'] = field['code']
                output_row[f'field_{i}_name'] = field['name']
                output_row[f'field_{i}_confidence'] = f"{field['percentage']:.2f}%"
            
            # Fill remaining fields if less than 6
            for i in range(len(result['fields']) + 1, 7):
                output_row[f'field_{i}_code'] = ''
                output_row[f'field_{i}_name'] = ''
                output_row[f'field_{i}_confidence'] = ''
            
            output_rows.append(output_row)
            
        except Exception as e:
            print(f"\n❌ Error processing row {idx + 1}: {e}")
            # Add empty fields on error
            output_row = {
                'title': title,
                'abstract': abstract
            }
            for i in range(1, 7):
                output_row[f'field_{i}_code'] = ''
                output_row[f'field_{i}_name'] = ''
                output_row[f'field_{i}_confidence'] = ''
            output_rows.append(output_row)
    
    # Create output DataFrame
    output_df = pd.DataFrame(output_rows)
    
    # Save to CSV
    try:
        output_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print()
        print("=" * 70)
        print("✅ CLASSIFICATION COMPLETE!")
        print("=" * 70)
        print(f"Processed: {len(df)} papers")
        print(f"Output saved to: {output_file}")
        print()
        print("Output columns:")
        print("  - title")
        print("  - abstract")
        for i in range(1, 7):
            print(f"  - field_{i}_code, field_{i}_name, field_{i}_confidence")
        print("=" * 70)
    except Exception as e:
        print(f"\n❌ Error saving output CSV: {e}")


def create_sample_csv():
    """Create a sample input CSV for testing"""
    sample_data = [
        {
            'title': 'Deep Learning for Medical Image Segmentation',
            'abstract': 'This paper presents a novel deep learning approach using U-Net architecture for automated medical image segmentation. We achieved 95% accuracy on CT scan datasets.'
        },
        {
            'title': 'Blockchain-Based Supply Chain Management System',
            'abstract': 'We propose a decentralized blockchain framework for supply chain traceability using smart contracts and IoT sensors to ensure transparency and security.'
        },
        {
            'title': 'Quantum Computing Algorithms for Optimization',
            'abstract': 'This research explores quantum algorithms for solving complex optimization problems, demonstrating quantum advantage over classical methods in specific scenarios.'
        }
    ]
    
    df = pd.DataFrame(sample_data)
    sample_file = 'sample_papers.csv'
    df.to_csv(sample_file, index=False, encoding='utf-8-sig')
    print(f"✅ Sample CSV created: {sample_file}")
    return sample_file


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Batch classify papers from CSV file')
    parser.add_argument('input_file', nargs='?', help='Input CSV file with title and abstract columns')
    parser.add_argument('-o', '--output', help='Output CSV file path (optional)')
    parser.add_argument('--sample', action='store_true', help='Create a sample CSV file for testing')
    
    args = parser.parse_args()
    
    if args.sample:
        # Create sample CSV
        sample_file = create_sample_csv()
        print()
        print("To process this sample file, run:")
        print(f"python batch_classify_csv.py {sample_file}")
    elif args.input_file:
        # Process the CSV file
        process_csv(args.input_file, args.output)
    else:
        # No arguments provided
        print("Batch Paper Classification Tool")
        print()
        print("Usage:")
        print("  python batch_classify_csv.py <input.csv>              # Process CSV")
        print("  python batch_classify_csv.py <input.csv> -o out.csv  # Specify output")
        print("  python batch_classify_csv.py --sample                # Create sample CSV")
        print()
        print("Required CSV columns: 'title' and 'abstract'")
        print("Output: CSV with title, abstract, and 6 field columns")
