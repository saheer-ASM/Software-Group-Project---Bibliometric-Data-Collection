"""Direct test of classifier without caching"""
import os
from dotenv import load_dotenv
from services.llm_field_classifier import LLMFieldClassifier

load_dotenv()

# Initialize classifier with caching disabled
classifier = LLMFieldClassifier(provider="openrouter", cache_enabled=False)

title = "A Review of Blockchain Technology in Knowledge-Defined Networking"
abstract = """Knowledge-Defined Networking (KDN) necessarily consists of a knowledge plane for 
the generation of knowledge, typically using machine learning techniques, and the dissemination 
of knowledge, in order to facilitate the optimization of the network. Blockchain is a 
disruptive technology that has the capacity to add immutability, transparency, and security 
to KDN."""

print("Testing classifier...")
print(f"Model: {classifier.model}")
print(f"Cache enabled: {classifier.cache_enabled}")
print()

try:
    result = classifier.classify(title, abstract)
    print(f"Success! Result:")
    for i, field in enumerate(result, 1):
        print(f"{i}. [{field['code']}] - {field['percentage']}%")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
