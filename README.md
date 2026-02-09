# Google Scholar & Scopus Publication Scraper

A powerful Python script that scrapes publications from Google Scholar and enriches them with Scopus data using Playwright for web automation.

## Features

✅ **Google Scholar Scraping** - Extracts all publications from an author's profile  
✅ **Playwright-based** - Modern, reliable web automation (replaced Selenium)  
✅ **Scopus Integration** - Fetches Scopus Author ID and publication metadata  
✅ **Excel Export** - Professional formatted Excel files with all data  
✅ **Command-line Interface** - Easy to use with author name as parameter  
✅ **Comprehensive Data** - Title, Abstract, Year, Citations, DOI, and more

## Installation

### 1. Install Python Dependencies

```powershell
pip install playwright openpyxl requests python-dotenv
```

### 2. Install Playwright Browsers

```powershell
playwright install chromium
```

### 3. Configure API Keys

Edit the `.env` file and add your API keys:

```env
# ScraperAPI Key (for Google Scholar)
key="your_scraperapi_key_here"

# Scopus API Key (Optional - Get from https://dev.elsevier.com/)
scopus_key="your_scopus_api_key_here"
```

#### Getting API Keys:

- **ScraperAPI**: Sign up at [https://www.scraperapi.com/](https://www.scraperapi.com/)
- **Scopus API**: Register at [https://dev.elsevier.com/](https://dev.elsevier.com/)

**Note:** The script works without Scopus API key, but you'll miss Scopus-specific data.

## Usage

### Basic Usage (Interactive)

```powershell
python main.py
```

You'll be prompted to enter the author name.

### Command-line Usage

```powershell
python main.py "John Smith"
```

Replace "John Smith" with any author name.

### Examples

```powershell
# Example 1: Full author name
python main.py "Kalupahana Liyanage Kushan Sudheera"

# Example 2: Common name
python main.py "Albert Einstein"

# Example 3: Without Scopus (still works)
python main.py "Marie Curie"
```

## Output

The script generates an Excel file with the following columns:

| Column | Description |
|--------|-------------|
| **No.** | Sequential number |
| **Author Name** | The author you searched for |
| **Scopus Author ID** | Unique Scopus identifier |
| **Publication Title** | Title of the publication |
| **Abstract** | Full abstract text |
| **Publication Year (Scholar)** | Year from Google Scholar |
| **Publication Year (Scopus)** | Year from Scopus (if found) |
| **Citations (Scholar)** | Citation count from Google Scholar |
| **Scopus Document ID** | Scopus document identifier |
| **Scopus EID** | Electronic Identifier from Scopus |
| **DOI** | Digital Object Identifier |

**Output filename format:**  
`publications_Author_Name_20260119_143025.xlsx`

## How It Works

1. **Search Google Scholar** - Uses ScraperAPI to find the author's profile
2. **Extract Publications** - Playwright scrapes all publications (clicks "Show more" automatically)
3. **Fetch Abstracts** - Opens each publication page to extract abstract
4. **Scopus Enrichment** - Queries Scopus API for additional metadata
5. **Export to Excel** - Creates formatted Excel file with all data

## Features Compared to Old Version

| Feature | Old (Selenium) | New (Playwright) |
|---------|---------------|------------------|
| Browser Automation | Selenium | ✅ Playwright (async) |
| Output Format | CSV | ✅ Excel (.xlsx) |
| Scopus Integration | ❌ No | ✅ Yes |
| Author Input | Hardcoded | ✅ Command-line arg |
| Citations Data | ❌ No | ✅ Yes |
| Year Extraction | ❌ No | ✅ Yes |
| Excel Formatting | ❌ No | ✅ Yes |
| Async Support | ❌ No | ✅ Yes |

## Troubleshooting

### "No search results found"
- Check if the author name is correct
- Try using full name or variations
- Verify ScraperAPI key is valid

### "Could not find author profile link"
- Author may not have Google Scholar profile
- Try searching manually on Google Scholar first

### Missing Scopus data
- Ensure `scopus_key` is set in `.env` file
- Check Scopus API quota (free tier has limits)
- Some publications may not be in Scopus database

### Playwright errors
- Run `playwright install chromium` again
- Check internet connection
- Increase timeout values if network is slow

## Advanced Configuration

### Change Browser Visibility

In `main.py`, find this line:
```python
browser = await p.chromium.launch(headless=False)
```

Change to `headless=True` to run without visible browser window.

### Adjust Timeouts

Modify timeout values (in milliseconds) in the code:
```python
await page.wait_for_selector(".gsc_a_at", timeout=10000)  # 10 seconds
```

## Requirements

- Python 3.7+
- Windows, macOS, or Linux
- Internet connection
- ScraperAPI account (free tier available)
- Scopus API key (optional, free for registered users)

## File Structure

```
selanium/
├── main.py              # Main script (Playwright version)
├── .env                 # API keys configuration
├── README.md            # This file
└── publications_*.xlsx  # Generated Excel files
```

## License

This project is for educational purposes. Respect Google Scholar and Scopus terms of service.

## Credits

**Author:** Shaith-Ahamed  
**Repository:** [github.com/Shaith-Ahamed/sinhala](https://github.com/Shaith-Ahamed/sinhala)

---

**Need Help?** Open an issue on GitHub or contact the author.
