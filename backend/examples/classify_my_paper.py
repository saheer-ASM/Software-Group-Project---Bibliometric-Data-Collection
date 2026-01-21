"""
Simple script to classify your own papers
Just add your title and abstract below
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


def classify_my_paper():
    """Classify your own paper"""
    
    # ========================================
    # ADD YOUR PAPER DETAILS HERE
    # ========================================
    
    title = "Nanometre-scale thermometry in a living cell"
    
    abstract = """
    Sensitive probing of temperature variations on nanometre scales is an outstanding challenge in many areas of modern science and technology1. In particular, a thermometer capable of subdegree temperature resolution over a large range of temperatures as well as integration within a living system could provide a powerful new tool in many areas of biological, physical and chemical research. Possibilities range from the temperature-induced control of gene expression2,3,4,5 and tumour metabolism6 to the cell-selective treatment of disease7,8 and the study of heat dissipation in integrated circuits1. By combining local light-induced heat sources with sensitive nanoscale thermometry, it may also be possible to engineer biological processes at the subcellular level2,3,4,5. Here we demonstrate a new approach to nanoscale thermometry that uses coherent manipulation of the electronic spin associated with nitrogen–vacancy colour centres in diamond. Our technique makes it possible to detect temperature variations as small as 1.8 mK (a sensitivity of 9 mK Hz−1/2) in an ultrapure bulk diamond sample. Using nitrogen–vacancy centres in diamond nanocrystals (nanodiamonds), we directly measure the local thermal environment on length scales as short as 200 nanometres. Finally, by introducing both nanodiamonds and gold nanoparticles into a single human embryonic fibroblast, we demonstrate temperature-gradient control and mapping at the subcellular level, enabling unique potential applications in life sciences.
    """
    
    # ========================================
    # CLASSIFICATION
    # ========================================
    
    print("=" * 70)
    print("PAPER FIELD CLASSIFICATION")
    print("=" * 70)
    
    # Initialize classifier
    classifier = LLMFieldClassifier(
        provider="openrouter",
        model="openai/gpt-4o-mini",
        cache_enabled=True
    )
    
    print(f"\nTitle: {title}\n")
    print(f"Abstract: {abstract[:200]}...\n")
    print("Classifying... please wait...\n")
    
    # Classify the paper
    result = classifier.classify(
        title=title,
        abstract=abstract,
        return_names=True
    )
    
    # Display results
    print("=" * 70)
    print("TOP 6 RESEARCH FIELDS WITH CONFIDENCE PERCENTAGES")
    print("=" * 70)
    
    for i, field in enumerate(result['fields'], 1):
        print(f"{i}. [{field['code']}] {field['name']}")
        print(f"   Confidence: {field['percentage']:.1f}%")
        
        # Visual progress bar
        bar_length = int(field['percentage'] / 2)  # Scale to 50 chars max
        bar = '█' * bar_length + '░' * (50 - bar_length)
        print(f"   [{bar}]\n")
    
    print("=" * 70)
    print("Classification complete!")
    print("=" * 70)


if __name__ == "__main__":
    classify_my_paper()
