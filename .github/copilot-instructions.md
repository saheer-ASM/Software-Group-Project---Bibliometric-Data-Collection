# Bibliometric Analysis System - Project Instructions

## Project Overview
This is a bibliometric analysis system for collecting and analyzing research data from 100,000 authors across 372 Scopus research fields.

## Technology Stack
- **Backend**: Python with Flask/FastAPI
- **Frontend**: React.js
- **Database**: PostgreSQL and MongoDB
- **Web Crawling**: scholarly, serpapi, pygscholar, BeautifulSoup, Selenium
- **Data Processing**: pandas, numpy, scikit-learn

## Key Features
1. Scopus API integration for author data retrieval
2. Google Scholar crawling for publication data
3. Field classification using keyword-based analysis of titles and abstracts
4. Citation and h-index calculation
5. Self-citation analysis
6. Author contribution analysis based on publication order
7. CSV export of bibliometric indicators
8. Web interface for data upload, processing, and visualization

## Development Guidelines
- Use type hints in Python code
- Follow PEP 8 style guidelines
- Write docstrings for all functions and classes
- Implement error handling and logging
- Use environment variables for API keys and credentials
- Optimize for scalability (100,000 authors)

## Project Status
✅ Step 1: Create copilot-instructions.md - COMPLETED
⏳ Step 2: Clarify project requirements - IN PROGRESS
⬜ Step 3: Scaffold project structure
⬜ Step 4: Create field classification module
⬜ Step 5: Set up backend structure
⬜ Step 6: Create requirements.txt
⬜ Step 7: Create documentation
