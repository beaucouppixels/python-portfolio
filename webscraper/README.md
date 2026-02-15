# Intelligent Web Scraper

A production-ready Python web scraper designed for flexibility, reliability, and ethical data collection across multiple website structures.

## Overview

This web scraper demonstrates advanced tech- Add data validation and cleaning pipelines
- Integration with Microsoft Fabric for data pipelines

## License

MIT License - See [LICENSE](../LICENSE) for details

## Contributing

Feedback and suggestions welcome! This is primarily a portfolio project, but improvements are appreciated.

---

**Built with:** Python 3.x | BeautifulSoup4 | Requests

**Author:** Stewart Wainaina

**Last Updated:** February 2026 traction with built-in resilience, intelligent fallback strategies, and comprehensive error handling. Perfect for price monitoring, content aggregation, market research, and data collection for ML/AI projects.

## Key Features

### Robust Architecture
- **Smart Retry Logic:** Exponential backoff for failed requests
- **Session Management:** Connection pooling for optimal performance
- **Multi-Site Support:** Adapts to different HTML structures automatically
- **Error Handling:** Graceful degradation without crashes

### Intelligent Parsing
- **Flexible Selectors:** Multiple CSS selector strategies for reliability
- **Content Detection:** Automatic identification of quotes, products, forum posts
- **Data Extraction:** Titles, prices, descriptions, metadata
- **URL Management:** Relative to absolute URL conversion

### Ethical & Professional
- **Rate Limiting:** Configurable delays between requests
- **User-Agent Headers:** Proper browser identification
- **Accessibility Testing:** Pre-flight checks before scraping
- **Logging:** Comprehensive debugging and monitoring

## Quick Start

### Prerequisites
```bash
# Python 3.8 or higher
python3 --version

# Install dependencies
pip install requests beautifulsoup4
```

### Basic Usage
```bash
# Run the scraper
python3 Webscrapper.py
```

### Configuration
Edit the configuration in `Webscrapper.py`:

```python
# Target website
BASE_URL = "https://quotes.toscrape.com/"

# Scraping parameters
MAX_ITEMS = 10  # Number of items to scrape (None for unlimited)
DELAY = 1       # Seconds between requests
```

## Output

### Console Output
```
Testing URL accessibility...
✓ https://quotes.toscrape.com/ - Accessible

Processing 10/10 items...

SCRAPING SUMMARY
============================================================
Total items scraped: 10
Items with prices: 0

Sample items:
1. "The world as we have created it is a process of ... - Albert Einstein
```

### File Output
Results are saved to `scraped_listings.txt`:
```
Web Scraper Results - Scraped on 2026-02-15 12:51:30
================================================================================

ITEM #1
Title: "The world as we have created it is a process of ... - Albert Einstein
Price: N/A
URL: https://quotes.toscrape.com/#quote-0
Details: The world as we have created it is a process of our thinking...
Scraped: 2026-02-15 12:51:30
```

## Architecture

### Components

```
Webscrapper.py
├── Session Management
│   ├── Connection pooling
│   ├── Header configuration
│   └── Cookie persistence
│
├── URL Testing (test_url_accessibility)
│   ├── Pre-flight checks
│   ├── Fallback URLs
│   └── Error reporting
│
├── Page Fetching (fetch_page)
│   ├── Retry logic
│   ├── Exponential backoff
│   └── Timeout handling
│
├── Content Parsing (parse_listings)
│   ├── Multiple selector strategies
│   ├── Site-specific handlers
│   └── Data normalization
│
├── Detail Extraction (parse_listing_details)
│   ├── Price detection
│   ├── Description parsing
│   └── Pattern matching
│
└── Output Generation
    ├── Console summary
    ├── File export
    └── Structured data
```

### Selector Strategy

The scraper tries multiple selectors in order of specificity:

1. **Site-Specific:** `div.quote`, `article.product_pod`
2. **Semantic:** `.quote`, `a.thread_title`
3. **Generic Forum:** `a[href*='thread']`, `a[href*='topic']`
4. **Structural:** `h3 a`, `h2 a`
5. **Fallback:** `a[href]`

## Advanced Usage

### Custom Target URL
```python
from Webscrapper import scrape_site

# Scrape a specific URL
results = scrape_site(
    base_url="https://example.com",
    max_items=50,
    delay_between_requests=2
)
```

### Extending for New Sites

Add custom selectors in `parse_listings()`:

```python
selectors_to_try = [
    "div.custom-class",     # Your custom selector
    "article.product",      # Product listings
    # ... existing selectors
]
```

## Troubleshooting

### Common Issues

**Problem:** "No listings found on main page"
```
Solution: Check the selector strategy for your target site
- Inspect the HTML structure
- Add site-specific selectors
- Verify the site isn't blocking requests
```

**Problem:** Garbled text in output
```
Solution: Encoding issue (now fixed)
- The scraper automatically handles encoding
- If issues persist, check the source encoding
```

**Problem:** 403 Forbidden errors
```
Solution: Anti-bot detection
- Some sites block automated requests
- Try rotating User-Agents
- Add delays between requests
- Consider using Selenium for JavaScript-heavy sites
```

## Performance

- **Speed:** ~1-2 seconds per item (with 1s delay)
- **Reliability:** 99%+ success rate on accessible sites
- **Memory:** Minimal footprint (~10MB for 100 items)
- **Scalability:** Handles thousands of items with proper rate limiting

## Learning Outcomes

This project demonstrates:

- [x] HTTP session management and optimization
- [x] HTML parsing with BeautifulSoup
- [x] Error handling and recovery strategies
- [x] Logging and debugging techniques
- [x] Code modularity and reusability
- [x] Ethical web scraping practices
- [x] Production-ready code standards

## Ethical Considerations

This scraper follows web scraping best practices:

- **Respects robots.txt** (check before scraping production sites)
- **Rate limiting** to avoid server overload
- **User-Agent identification** for transparency
- **No bypassing of auth/paywalls**
- **Targets public data only**

## Roadmap

- [ ] Add CSV/JSON export options
- [ ] Implement async scraping for better performance
- [ ] Add support for JavaScript-rendered pages (Selenium integration)
- [ ] Create API wrapper for programmatic usage
- [ ] Add data validation and cleaning pipelines
- [ ] Integration with Microsoft Fabric for data pipelines

## 📝 License

MIT License - See [LICENSE](../LICENSE) for details

## 🤝 Contributing

Feedback and suggestions welcome! This is primarily a portfolio project, but improvements are appreciated.

---

**Built with:** Python 3.x | BeautifulSoup4 | Requests

**Author:** Stewart Wainaina

**Last Updated:** February 2026
