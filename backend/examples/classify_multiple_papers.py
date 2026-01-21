"""
Classify multiple papers at once
Add your papers to the list below
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
root_dir = Path(__file__).parent.parent.parent
env_path = root_dir / '.env'
load_dotenv(env_path)

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from services.llm_field_classifier import LLMFieldClassifier


def classify_multiple_papers():
    """Classify multiple papers"""
    
    # ========================================
    # ADD YOUR PAPERS HERE
    # ========================================
    
    papers = [
        {
            "title": "First paper title",
            "abstract": "First paper abstract..."
        },
        {
            "title": "Second paper title",
            "abstract": "Second paper abstract..."
        },
        {
            "title": "Third paper title",
            "abstract": "Third paper abstract..."
        }
        # Add more papers here...
    ]
    
    # ========================================
    # CLASSIFICATION
    # ========================================
    
    print("=" * 70)
    print(f"CLASSIFYING {len(papers)} PAPERS")
    print("=" * 70)
    
    # Initialize classifier
    classifier = LLMFieldClassifier(
        provider="openrouter",
        model="openai/gpt-4o-mini",
        cache_enabled=True
    )
    
    # Classify all papers
    results = classifier.classify_batch(papers)
    
    # Display results
    print("\n" + "=" * 70)
    print("CLASSIFICATION RESULTS")
    print("=" * 70)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print("-" * 70)
        
        if result['status'] == 'success':
            print("Top 6 Fields with Confidence:")
            for field in result['fields']:
                print(f"   [{field['code']}] {field['name']} - {field['percentage']:.1f}%")
        else:
            print(f"   Error: {result.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 70)
    print("All papers classified!")
    print("=" * 70)


if __name__ == "__main__":
    classify_multiple_papers()
