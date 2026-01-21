"""
Example script demonstrating the LLM Field Classifier
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file in the root directory
root_dir = Path(__file__).parent.parent.parent
env_path = root_dir / '.env'
load_dotenv(env_path)

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from services.llm_field_classifier import LLMFieldClassifier


def example_single_paper():
    """Example: Classify a single paper"""
    print("=" * 60)
    print("EXAMPLE 1: Single Paper Classification")
    print("=" * 60)
    
    # Sample paper
    paper = {
        "title": "Deep Learning Approaches for COVID-19 Detection from Chest X-Ray Images",
        "abstract": "The COVID-19 pandemic has highlighted the need for rapid and accurate diagnostic tools. This study presents a deep learning framework using convolutional neural networks (CNNs) for automated detection of COVID-19 from chest X-ray images. We trained our model on a dataset of 10,000 images and achieved 95% accuracy. The proposed method can assist radiologists in making faster diagnoses and help manage the overwhelming number of cases during the pandemic."
    }
    
    # Initialize classifier (using OpenRouter with free tier)
    classifier = LLMFieldClassifier(
        provider="openrouter",
        model="openai/gpt-4o-mini",
        cache_enabled=True
    )
    
    # Classify the paper
    result = classifier.classify(
        title=paper['title'],
        abstract=paper['abstract'],
        return_names=True
    )
    
    print(f"\nTitle: {paper['title']}\n")
    print("Top 6 Research Fields:")
    for i, (code, name) in enumerate(zip(result['field_codes'], result['field_names']), 1):
        print(f"  {i}. [{code}] {name}")
    
    return classifier


def example_batch_classification(classifier):
    """Example: Classify multiple papers"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Batch Classification")
    print("=" * 60)
    
    papers = [
        {
            "title": "Machine Learning for Stock Price Prediction",
            "abstract": "This paper explores the use of machine learning algorithms including LSTM and random forests for predicting stock market prices. We analyze historical data and demonstrate improved prediction accuracy."
        },
        {
            "title": "Climate Change Impact on Coral Reef Ecosystems",
            "abstract": "We investigate the effects of rising ocean temperatures on coral reef biodiversity. Our study shows significant coral bleaching and species loss in affected regions."
        },
        {
            "title": "CRISPR-Cas9 Gene Editing in Cancer Therapy",
            "abstract": "This research demonstrates the potential of CRISPR-Cas9 technology for targeted cancer treatment. We successfully edited oncogenes in tumor cells, showing promising results in reducing cancer cell proliferation."
        }
    ]
    
    print(f"\nClassifying {len(papers)} papers...\n")
    
    results = classifier.classify_batch(papers)
    
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title'][:60]}...")
        print(f"   Fields: {result['field_codes']}")
        print(f"   Status: {result['status']}\n")
    
    return results


def example_cost_estimation():
    """Example: Estimate costs for large-scale processing"""
    print("=" * 60)
    print("EXAMPLE 3: Cost Estimation")
    print("=" * 60)
    
    # Compare costs for different providers
    providers = [
        ("openrouter", "openai/gpt-4o-mini"),
    ]
    
    paper_counts = [100, 1000, 10000, 100000]
    
    print("\nCost Comparison for Different Scales:\n")
    
    for provider, model in providers:
        try:
            classifier = LLMFieldClassifier(provider=provider, model=model)
            print(f"{provider.upper()} - {model}")
            print("-" * 60)
            
            for count in paper_counts:
                estimate = classifier.estimate_cost(count)
                print(f"  {count:>6} papers: ${estimate['total_cost']:>8.2f} "
                      f"(${estimate['cost_per_paper']:.4f}/paper)")
            print()
        except Exception as e:
            print(f"Skipping {provider}: {str(e)}\n")


def example_with_cache():
    """Example: Demonstrate caching benefits"""
    print("=" * 60)
    print("EXAMPLE 4: Caching Demonstration")
    print("=" * 60)
    
    paper = {
        "title": "Quantum Computing Applications in Cryptography",
        "abstract": "This paper explores how quantum computing threatens current cryptographic systems and proposes quantum-resistant algorithms for future security."
    }
    
    classifier = LLMFieldClassifier(provider="openrouter", cache_enabled=True)
    
    print("\nFirst classification (API call)...")
    result1 = classifier.classify(paper['title'], paper['abstract'])
    print(f"Result: {result1}")
    
    print("\nSecond classification (from cache)...")
    result2 = classifier.classify(paper['title'], paper['abstract'])
    print(f"Result: {result2}")
    
    print("\nCache saved time and money on the second call!")


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("LLM FIELD CLASSIFIER - EXAMPLES")
    print("=" * 60)
    
    # Check for API keys
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        print("\n⚠️  WARNING: No API keys found!")
        print("Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable")
        print("\nFor testing purposes, examples will show the structure without API calls.\n")
    
    try:
        # Example 1: Single paper
        classifier = example_single_paper()
        
        # Example 2: Batch processing
        example_batch_classification(classifier)
        
        # Example 3: Cost estimation
        example_cost_estimation()
        
        # Example 4: Caching
        example_with_cache()
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nMake sure you have set up your API keys in the .env file")
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
