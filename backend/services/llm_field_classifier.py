"""
LLM-based Field Classifier using OpenAI and Claude APIs
Optimized for accuracy and budget-friendliness
"""

import os
import json
import hashlib
from typing import List, Dict, Optional
from openai import OpenAI
import anthropic
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)


class LLMFieldClassifier:
    """
    Classifies research papers into Scopus fields using LLM APIs
    Includes caching and cost optimization strategies
    """
    
    def __init__(
        self, 
        provider: str = "openai",  # "openai", "claude", or "openrouter"
        cache_enabled: bool = True,
        model: Optional[str] = None
    ):
        """
        Initialize the classifier
        
        Args:
            provider: "openai", "claude", or "openrouter"
            cache_enabled: Enable caching to avoid duplicate API calls
            model: Specific model to use (defaults to cost-effective options)
        """
        self.provider = provider
        self.cache_enabled = cache_enabled
        self.cache = {}
        
        # Initialize API clients
        if provider == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = model or "gpt-4o-mini"  # Most cost-effective
        elif provider == "openrouter":
            # OpenRouter uses OpenAI client but with different base URL
            self.client = OpenAI(
                api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1",
                default_headers={
                    "HTTP-Referer": "http://localhost:5000",  # Optional, for rankings
                    "X-Title": "Bibliometric Analysis System"  # Optional, for rankings
                }
            )
            self.model = model or "openai/gpt-4o-mini"  # Cost-effective via OpenRouter
        elif provider == "claude":
            self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model = model or "claude-3-haiku-20240307"  # Most cost-effective
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        
        # Load Scopus fields
        self.scopus_fields = self._load_scopus_fields()
    
    def _load_scopus_fields(self) -> Dict[int, str]:
        """Load Scopus field codes and descriptions"""
        try:
            from .scopus_fields import SCOPUS_FIELDS
            return SCOPUS_FIELDS
        except ImportError:
            # Fallback: load from file if module not available
            logger.warning("Could not import SCOPUS_FIELDS, using inline data")
            return {}
    
    def _get_cache_key(self, title: str, abstract: str) -> str:
        """Generate cache key from title and abstract"""
        content = f"{title}|{abstract}".lower().strip()
        return hashlib.md5(content.encode()).hexdigest()
    
    def _create_prompt(self, title: str, abstract: str) -> str:
        """
        Create optimized prompt for field classification
        Shorter prompts = lower cost
        """
        # Create a detailed field list with specific codes and names
        field_summary = """
You must choose from these SPECIFIC Scopus field codes (372 detailed fields). DO NOT use general codes ending in "00" (like 1700, 2200, 2700).

Computer Science (1700s):
1702-Artificial Intelligence, 1703-Computational Theory and Mathematics, 1704-Computer Graphics and CAD, 1705-Computer Networks and Communications, 1706-Computer Science Applications, 1707-Computer Vision and Pattern Recognition, 1708-Hardware and Architecture, 1709-Human-Computer Interaction, 1710-Information Systems, 1711-Signal Processing, 1712-Software

Engineering (2200s):
2202-Aerospace Engineering, 2203-Automotive Engineering, 2204-Biomedical Engineering, 2205-Civil and Structural Engineering, 2206-Computational Mechanics, 2207-Control and Systems Engineering, 2208-Electrical and Electronic Engineering, 2209-Industrial and Manufacturing Engineering, 2210-Mechanical Engineering, 2211-Mechanics of Materials, 2212-Ocean Engineering, 2213-Safety Risk Reliability and Quality, 2214-Media Technology, 2215-Building and Construction, 2216-Architecture

Mathematics (2600s):
2602-Algebra and Number Theory, 2603-Analysis, 2604-Applied Mathematics, 2605-Computational Mathematics, 2606-Control and Optimization, 2607-Discrete Mathematics and Combinatorics, 2608-Geometry and Topology, 2609-Logic, 2610-Mathematical Physics, 2611-Modeling and Simulation, 2612-Numerical Analysis, 2613-Statistics and Probability, 2614-Theoretical Computer Science

Medicine (2700s):
2703-Anesthesiology and Pain Medicine, 2704-Biochemistry (medical), 2705-Cardiology and Cardiovascular Medicine, 2708-Dermatology, 2711-Emergency Medicine, 2712-Endocrinology Diabetes and Metabolism, 2713-Epidemiology, 2715-Gastroenterology, 2716-Genetics (clinical), 2718-Health Informatics, 2719-Health Policy, 2724-Internal Medicine, 2725-Infectious Diseases, 2728-Neurology (clinical), 2729-Obstetrics and Gynecology, 2730-Oncology, 2731-Ophthalmology, 2738-Psychiatry and Mental Health, 2739-Public Health Environmental and Occupational Health, 2741-Radiology Nuclear Medicine and Imaging, 2746-Surgery

Agricultural/Biological (1100s):
1102-Agronomy and Crop Science, 1103-Animal Science and Zoology, 1104-Aquatic Science, 1105-Ecology Evolution Behavior and Systematics, 1106-Food Science, 1107-Forestry, 1108-Horticulture, 1109-Insect Science, 1110-Plant Science, 1111-Soil Science

Biochemistry/Genetics (1300s):
1302-Aging, 1303-Biochemistry, 1304-Biophysics, 1305-Biotechnology, 1306-Cancer Research, 1307-Cell Biology, 1309-Developmental Biology, 1310-Endocrinology, 1311-Genetics, 1312-Molecular Biology, 1313-Molecular Medicine, 1314-Physiology

Business/Management (1400s):
1402-Accounting, 1403-Business and International Management, 1404-Management Information Systems, 1405-Management of Technology and Innovation, 1406-Marketing, 1407-Organizational Behavior and HR Management, 1408-Strategy and Management, 1409-Tourism Leisure and Hospitality Management

Environmental Science (2300s):
2302-Ecological Modeling, 2303-Ecology, 2304-Environmental Chemistry, 2305-Environmental Engineering, 2306-Global and Planetary Change, 2307-Health Toxicology and Mutagenesis, 2308-Management Monitoring Policy and Law, 2310-Pollution, 2311-Waste Management and Disposal, 2312-Water Science and Technology

Energy (2100s):
2102-Energy Engineering and Power Technology, 2103-Fuel Technology, 2104-Nuclear Energy and Engineering, 2105-Renewable Energy Sustainability and the Environment

Materials Science (2500s):
2502-Biomaterials, 2503-Ceramics and Composites, 2504-Electronic Optical and Magnetic Materials, 2505-Materials Chemistry, 2506-Metals and Alloys, 2507-Polymers and Plastics, 2508-Surfaces Coatings and Films

Social Sciences (3300s):
3302-Archeology, 3303-Development, 3304-Education, 3305-Geography Planning and Development, 3306-Health (social science), 3308-Law, 3310-Linguistics and Language, 3312-Sociology and Political Science, 3313-Transportation, 3314-Anthropology, 3315-Communication, 3320-Political Science and International Relations

Physics (3100s):
3102-Acoustics and Ultrasonics, 3103-Astronomy and Astrophysics, 3104-Condensed Matter Physics, 3105-Instrumentation, 3106-Nuclear and High Energy Physics, 3107-Atomic and Molecular Physics and Optics, 3108-Radiation, 3109-Statistical and Nonlinear Physics

Chemistry (1600s), Earth Sciences (1900s), Economics (2000s), Immunology (2400s), Neuroscience (2800s), Nursing (2900s), Pharmacology (3000s), Psychology (3200s), and other specific fields (1200s-Arts, 1500s-Chemical Engineering, 1800s-Decision Sciences, 3400s-Veterinary, 3500s-Dentistry, 3600s-Health Professions) are also available.

CRITICAL: Choose ONLY 4-digit specific codes (e.g., 1702, 1705, 2208, 2611), NEVER general 2-digit codes ending in "00" (e.g., 1700, 2200).
"""
        
        # Enhanced prompt with reasoning steps and few-shot examples
        prompt = f"""You are an expert research field classifier specializing in Scopus taxonomy. Analyze this research paper deeply and identify the 6 most relevant SPECIFIC Scopus research fields.

## Paper to Classify:
Title: {title}

Abstract: {abstract}

## Available Scopus Fields:
{field_summary}

## Classification Instructions:
1. Read the title and abstract carefully to understand:
   - Main research objectives and methodology
   - Key technologies, algorithms, or theories used
   - Application domains and target problems
   - Interdisciplinary connections

2. Match paper content to SPECIFIC 4-digit field codes:
   - Identify primary methodology field (e.g., 1702 for AI algorithms)
   - Identify application domain field (e.g., 1705 for networking)
   - Identify supporting fields (e.g., 2208 for hardware, 2611 for simulation)
   - Consider interdisciplinary aspects

3. Assign confidence percentages (total=100%):
   - Primary field: 25-40%
   - Secondary field: 20-30%
   - Supporting fields: 10-20% each
   - Minor relevant fields: 5-10% each

## Few-Shot Examples:

Example 1:
Title: "Deep Learning for Medical Image Segmentation: A Survey"
Abstract: "This survey reviews deep learning techniques for medical image segmentation, including U-Net, FCN, and attention mechanisms..."
Result: [{{"code": 1702, "percentage": 35}}, {{"code": 2741, "percentage": 25}}, {{"code": 1707, "percentage": 20}}, {{"code": 2718, "percentage": 10}}, {{"code": 1706, "percentage": 6}}, {{"code": 2730, "percentage": 4}}]
Reasoning: 1702 (AI) is primary methodology, 2741 (Radiology) is application domain, 1707 (Graphics/Vision) for image processing, 2718 (Health Informatics) for medical data, 1706 (Hardware) for implementation, 2730 (Oncology) as potential application.

Example 2:
Title: "Blockchain-Based Supply Chain Management: Challenges and Solutions"
Abstract: "This paper proposes a blockchain architecture for supply chain traceability using smart contracts and IoT sensors..."
Result: [{{"code": 1710, "percentage": 30}}, {{"code": 1408, "percentage": 25}}, {{"code": 1705, "percentage": 20}}, {{"code": 2208, "percentage": 12}}, {{"code": 1706, "percentage": 8}}, {{"code": 1712, "percentage": 5}}]
Reasoning: 1710 (Information Systems) for blockchain systems, 1408 (Strategy/Management) for supply chain, 1705 (Networks) for distributed systems, 2208 (Electronics) for IoT, 1706 (Hardware) for sensors, 1712 (Software) for smart contracts.

## CRITICAL Rules:
- Use ONLY SPECIFIC 4-digit codes (1702, 1705, 2208, etc.)
- NEVER use general 2-digit codes ending in "00" (1700, 2200, 2700)
- Percentages must sum to exactly 100%
- Return ONLY valid JSON array format

## Your Response (JSON only):
"""
        
        return prompt
    
    def classify_with_openai(self, title: str, abstract: str) -> List[Dict]:
        """Classify using OpenAI API - returns list of dicts with code and percentage"""
        prompt = self._create_prompt(title, abstract)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a research field classification expert. Return only valid JSON with field codes and percentages."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # Low temperature for consistent results
                max_tokens=150,   # Increased for percentage data
                response_format={"type": "json_object"} if "gpt-4" in self.model else None
            )
            
            result = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if result.startswith('```'):
                # Extract content between ```json and ```
                import re
                json_match = re.search(r'```(?:json)?\s*(\[.*?\])\s*```', result, re.DOTALL)
                if json_match:
                    result = json_match.group(1)
                else:
                    # Try without json tag
                    result = result.replace('```json', '').replace('```', '').strip()
            
            # Parse the response
            if result.startswith('['):
                fields_data = json.loads(result)
            else:
                # Try to extract JSON array from response
                result_json = json.loads(result)
                fields_data = result_json.get('fields', result_json.get('data', []))
            
            # Ensure we have exactly 6 fields with percentages
            fields_data = fields_data[:6]
            
            # Validate and normalize percentages
            total_percentage = sum(item.get('percentage', 0) for item in fields_data)
            if total_percentage == 0:
                # If no percentages, assign equal weights
                for item in fields_data:
                    item['percentage'] = 100 / len(fields_data)
            elif total_percentage != 100:
                # Normalize to 100%
                for item in fields_data:
                    item['percentage'] = (item.get('percentage', 0) / total_percentage) * 100
            
            # Fill missing fields
            while len(fields_data) < 6:
                remaining_percent = 100 - sum(item['percentage'] for item in fields_data)
                fields_data.append({"code": 1000, "percentage": max(remaining_percent, 5)})
            
            logger.info(f"Classified paper: {title[:50]}... -> {fields_data}")
            return fields_data
            
        except Exception as e:
            logger.error(f"OpenAI classification error: {str(e)}")
            # Return default with equal percentages
            return [{"code": 1000, "percentage": 16.67} for _ in range(6)]
    
    def classify_with_claude(self, title: str, abstract: str) -> List[int]:
        """Classify using Claude API"""
        prompt = self._create_prompt(title, abstract)
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=100,  # Short response = lower cost
                temperature=0.1,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            result = response.content[0].text.strip()
            
            # Parse the response
            if result.startswith('['):
                fields = json.loads(result)
            else:
                # Try to extract JSON array from response
                import re
                match = re.search(r'\[[\d,\s]+\]', result)
                if match:
                    fields = json.loads(match.group())
                else:
                    fields = json.loads(result)
            
            # Ensure we have exactly 6 fields
            fields = fields[:6]
            while len(fields) < 6:
                fields.append(1000)  # Multidisciplinary as fallback
            
            logger.info(f"Classified paper: {title[:50]}... -> {fields}")
            return fields
            
        except Exception as e:
            logger.error(f"Claude classification error: {str(e)}")
            return [1000, 1000, 1000, 1000, 1000, 1000]
    
    def classify(
        self, 
        title: str, 
        abstract: str,
        return_names: bool = False
    ) -> List[int] | Dict[str, any]:
        """
        Classify a paper into top 6 Scopus fields
        
        Args:
            title: Paper title
            abstract: Paper abstract
            return_names: If True, return dict with codes and names
            
        Returns:
            List of 6 field codes or dict with codes and names
        """
        # Check cache first
        if self.cache_enabled:
            cache_key = self._get_cache_key(title, abstract)
            if cache_key in self.cache:
                logger.info("Using cached classification")
                fields = self.cache[cache_key]
                if not return_names:
                    return fields
                return self._format_with_names(fields)
        
        # Classify based on provider
        if self.provider == "openai" or self.provider == "openrouter":
            fields = self.classify_with_openai(title, abstract)
        elif self.provider == "claude":
            fields = self.classify_with_claude(title, abstract)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
        
        # Cache the result
        if self.cache_enabled:
            self.cache[cache_key] = fields
        
        # Return results
        if return_names:
            return self._format_with_names(fields)
        return fields
    
    def _format_with_names(self, fields_data: List[Dict]) -> Dict[str, any]:
        """Format field data with their names"""
        return {
            "fields": [
                {
                    "code": item['code'],
                    "name": self.scopus_fields.get(item['code'], f"Unknown ({item['code']})"),
                    "percentage": round(item['percentage'], 2)
                }
                for item in fields_data
            ]
        }
    
    def classify_batch(
        self, 
        papers: List[Dict[str, str]],
        batch_size: int = 10
    ) -> List[Dict[str, any]]:
        """
        Classify multiple papers with progress tracking
        
        Args:
            papers: List of dicts with 'title' and 'abstract' keys
            batch_size: Number of papers to process before logging progress
            
        Returns:
            List of classification results
        """
        results = []
        total = len(papers)
        
        for i, paper in enumerate(papers, 1):
            try:
                fields = self.classify(
                    paper['title'],
                    paper['abstract'],
                    return_names=True
                )
                
                results.append({
                    'title': paper['title'],
                    'field_codes': fields['field_codes'],
                    'field_names': fields['field_names'],
                    'status': 'success'
                })
                
            except Exception as e:
                logger.error(f"Error classifying paper {i}: {str(e)}")
                results.append({
                    'title': paper.get('title', 'Unknown'),
                    'field_codes': [1000] * 6,
                    'field_names': ['Multidisciplinary'] * 6,
                    'status': 'error',
                    'error': str(e)
                })
            
            # Progress update
            if i % batch_size == 0 or i == total:
                logger.info(f"Processed {i}/{total} papers")
        
        return results
    
    def estimate_cost(self, num_papers: int) -> Dict[str, float]:
        """
        Estimate API costs for classifying papers
        
        Args:
            num_papers: Number of papers to classify
            
        Returns:
            Dict with cost estimates
        """
        # Average tokens per request (prompt + response)
        avg_prompt_tokens = 400
        avg_completion_tokens = 50
        
        if self.provider == "openai":
            if "gpt-4o-mini" in self.model:
                # $0.150 / 1M input tokens, $0.600 / 1M output tokens
                input_cost = (avg_prompt_tokens * num_papers / 1_000_000) * 0.150
                output_cost = (avg_completion_tokens * num_papers / 1_000_000) * 0.600
            else:
                # GPT-4 pricing (more expensive)
                input_cost = (avg_prompt_tokens * num_papers / 1_000_000) * 10
                output_cost = (avg_completion_tokens * num_papers / 1_000_000) * 30
        
        elif self.provider == "claude":
            if "haiku" in self.model:
                # $0.25 / 1M input tokens, $1.25 / 1M output tokens
                input_cost = (avg_prompt_tokens * num_papers / 1_000_000) * 0.25
                output_cost = (avg_completion_tokens * num_papers / 1_000_000) * 1.25
            else:
                # Sonnet pricing (more expensive)
                input_cost = (avg_prompt_tokens * num_papers / 1_000_000) * 3
                output_cost = (avg_completion_tokens * num_papers / 1_000_000) * 15
        
        total_cost = input_cost + output_cost
        
        return {
            "num_papers": num_papers,
            "input_cost": round(input_cost, 2),
            "output_cost": round(output_cost, 2),
            "total_cost": round(total_cost, 2),
            "cost_per_paper": round(total_cost / num_papers, 4),
            "provider": self.provider,
            "model": self.model
        }


# Example usage
if __name__ == "__main__":
    # Example paper
    paper = {
        "title": "Deep Learning for Image Recognition using Convolutional Neural Networks",
        "abstract": "This paper presents a novel approach to image recognition using deep convolutional neural networks. We demonstrate improved accuracy on benchmark datasets and discuss applications in computer vision."
    }
    
    # Initialize classifier (cost-effective option)
    classifier = LLMFieldClassifier(provider="openai", model="gpt-4o-mini")
    
    # Classify single paper
    result = classifier.classify(
        paper['title'],
        paper['abstract'],
        return_names=True
    )
    
    print("Classification Result:")
    print(f"Field Codes: {result['field_codes']}")
    print(f"Field Names: {result['field_names']}")
    
    # Estimate costs for 1000 papers
    cost_estimate = classifier.estimate_cost(1000)
    print(f"\nCost for 1000 papers: ${cost_estimate['total_cost']}")
    print(f"Cost per paper: ${cost_estimate['cost_per_paper']}")
