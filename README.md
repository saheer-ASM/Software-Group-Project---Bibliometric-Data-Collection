# Bibliometric Analysis System

A scalable web application for collecting, processing, and analyzing bibliometric data from 100,000+ researchers across 372 Scopus research fields.

## Features

- **LLM-Powered Field Classification**: Uses OpenAI GPT-4o-mini or Claude Haiku to accurately classify papers into top 6 research fields
- **Cost-Optimized**: Intelligent caching and batch processing to minimize API costs
- **Scopus Integration**: Retrieve author data from Scopus API
- **Google Scholar Crawling**: Extract publication data, citations, and h-index
- **Bibliometric Calculations**: Citation analysis, self-citations, author contributions
- **CSV Export**: Export processed data for further analysis
- **Web Interface**: User-friendly interface for data upload and visualization

## Project Structure

```
Software Project/
├── backend/
│   ├── app.py                      # Flask application entry point
│   ├── config.py                   # Configuration settings
│   ├── services/
│   │   ├── llm_field_classifier.py # LLM-based field classifier
│   │   └── scopus_fields.py        # 372 Scopus field definitions
│   ├── models/                     # Database models
│   ├── crawlers/                   # Web scrapers
│   ├── utils/                      # Utility functions
│   └── examples/
│       └── test_classifier.py      # Example usage and tests
├── frontend/                       # React.js frontend (to be added)
├── data/                          # Data storage
├── .env.example                   # Environment variables template
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Installation

### Prerequisites
- Python 3.9+
- Node.js 16+ (for frontend)
- PostgreSQL
- MongoDB

### Setup

1. **Clone or navigate to the project directory**

2. **Create a virtual environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```powershell
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```
   OPENAI_API_KEY=your-openai-api-key
   ANTHROPIC_API_KEY=your-anthropic-api-key
   SCOPUS_API_KEY=your-scopus-api-key
   ```

## Usage

### Field Classification Examples

Run the example script to see the classifier in action:

```powershell
cd backend
python examples/test_classifier.py
```

### Using the Classifier in Your Code

```python
from services.llm_field_classifier import LLMFieldClassifier

# Initialize classifier (OpenAI GPT-4o-mini is most cost-effective)
classifier = LLMFieldClassifier(
    provider="openai",
    model="gpt-4o-mini",
    cache_enabled=True
)

# Classify a single paper
result = classifier.classify(
    title="Your paper title",
    abstract="Your paper abstract",
    return_names=True
)

print(f"Field Codes: {result['field_codes']}")
print(f"Field Names: {result['field_names']}")

# Classify multiple papers
papers = [
    {"title": "...", "abstract": "..."},
    {"title": "...", "abstract": "..."}
]
results = classifier.classify_batch(papers)

# Estimate costs
cost_estimate = classifier.estimate_cost(num_papers=1000)
print(f"Cost for 1000 papers: ${cost_estimate['total_cost']}")
```

### Starting the Flask API

```powershell
cd backend
python app.py
```

API will be available at `http://localhost:5000`

**Available Endpoints:**
- `GET /api/health` - Health check
- `POST /api/classify-fields` - Classify a paper's fields
- `POST /api/process-authors` - Process batch of authors

## Cost Analysis

### Cost Comparison (per 1000 papers)

| Provider | Model | Cost | Per Paper |
|----------|-------|------|-----------|
| OpenAI | gpt-4o-mini | **$0.30** | **$0.0003** |
| Claude | claude-3-haiku | $0.56 | $0.0006 |

**For 100,000 papers:**
- OpenAI GPT-4o-mini: ~$30
- Claude Haiku: ~$56

### Cost Optimization Strategies

1. **Caching**: Avoid re-processing identical papers
2. **Batch Processing**: Process in batches with progress tracking
3. **Short Prompts**: Optimized prompt design reduces token usage
4. **Low Temperature**: Consistent results with fewer retries

## Scopus Fields

The system classifies papers into 372 Scopus research fields organized into major categories:

- 1000s: Multidisciplinary, Agricultural/Biological Sciences, Arts & Humanities
- 1300s-1600s: Biochemistry, Business, Chemical Engineering, Chemistry
- 1700s-2000s: Computer Science, Decision Sciences, Earth Sciences, Economics
- 2100s-2600s: Energy, Engineering, Environmental Science, Immunology, Materials, Mathematics
- 2700s-3000s: Medicine, Neuroscience, Nursing, Pharmacology
- 3100s-3600s: Physics, Psychology, Social Sciences, Veterinary, Dentistry, Health Professions

See [scopus_fields.py](backend/services/scopus_fields.py) for the complete list.

## Development Timeline

- **Month 1**: ✅ Project setup, architecture design
- **Month 2**: Scopus API integration & data retrieval
- **Month 3**: Google Scholar crawling
- **Month 4**: ✅ Field classification & metrics
- **Month 5**: Web application development
- **Month 6**: Testing, documentation, deployment

## Technologies

- **Backend**: Python, Flask
- **LLM APIs**: OpenAI GPT-4o-mini, Claude Haiku
- **Data Processing**: pandas, numpy
- **Web Crawling**: BeautifulSoup, Selenium, scholarly
- **Databases**: PostgreSQL, MongoDB
- **Frontend**: React.js (coming soon)

## Contributing

This is a university project for Semester 5 Software Engineering course.

## License

Academic project - University of Ruhuna, Computer Engineering

## Contact

For questions or issues, please contact the development team.

---

**Note**: Make sure to obtain proper API keys and respect rate limits when crawling academic databases.
