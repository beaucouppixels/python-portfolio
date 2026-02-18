#!/usr/bin/env python3
"""
Universal Web Scraper
Supports both simple requests-based scraping and Selenium browser automation
"""

import requests
import time
import logging
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Try to import Selenium (optional)
try:
    from selenium import webdriver
    from selenium.webdriver.safari.options import Options as SafariOptions
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    logger.warning("Selenium not available. Browser automation features disabled.")


class WebScraper:
    """
    Universal web scraper supporting multiple strategies
    """
    
    def __init__(self, scraping_method='requests'):
        """
        Initialize scraper
        
        Args:
            scraping_method: 'requests' for simple HTTP, 'selenium' for browser automation
        """
        self.scraping_method = scraping_method
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        })
        self.driver = None
    
    def setup_selenium_driver(self):
        """Setup Safari WebDriver for Selenium scraping"""
        if not SELENIUM_AVAILABLE:
            raise ImportError("Selenium is not installed. Install with: pip3 install selenium")
        
        logger.info("Initializing Safari WebDriver...")
        options = SafariOptions()
        self.driver = webdriver.Safari(options=options)
        return self.driver
    
    def fetch_page_requests(self, url, max_retries=3):
        """
        Fetch page using requests (fast, simple sites)
        
        Args:
            url: URL to fetch
            max_retries: Number of retry attempts
            
        Returns:
            HTML content as string
        """
        for attempt in range(max_retries):
            try:
                logger.info("Fetching: %s (attempt %d)", url, attempt + 1)
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response.text
            except requests.exceptions.RequestException as e:
                logger.warning("Attempt %d failed for %s: %s", attempt + 1, url, str(e))
                if attempt < max_retries - 1:
                    time.sleep(2 * (attempt + 1))
                else:
                    logger.error("Failed to fetch %s after %d attempts", url, max_retries)
                    raise
        return None
    
    def fetch_page_selenium(self, url, wait_time=3):
        """
        Fetch page using Selenium (for JavaScript-heavy sites)
        
        Args:
            url: URL to fetch
            wait_time: Time to wait for page to load
            
        Returns:
            HTML content as string
        """
        if not self.driver:
            self.setup_selenium_driver()
        
        logger.info("Navigating to %s with Selenium...", url)
        self.driver.get(url)
        
        # Wait for page to load
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except Exception as e:
            logger.warning("Timeout waiting for page load: %s", str(e))
        
        # Give page time to fully render
        time.sleep(wait_time)
        
        # Optional: scroll to trigger lazy-loaded content
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        
        return self.driver.page_source
    
    def fetch_page(self, url, **kwargs):
        """
        Fetch page using configured method
        
        Args:
            url: URL to fetch
            **kwargs: Additional arguments for fetch method
            
        Returns:
            HTML content as string
        """
        if self.scraping_method == 'selenium':
            return self.fetch_page_selenium(url, **kwargs)
        else:
            return self.fetch_page_requests(url, **kwargs)
    
    def parse_generic_listings(self, html, base_url, selectors, filters=None):
        """
        Generic parser for listing pages
        
        Args:
            html: HTML content
            base_url: Base URL for building full URLs
            selectors: List of (selector, description) tuples to try
            filters: Optional dict with filter functions
            
        Returns:
            List of listing dictionaries
        """
        soup = BeautifulSoup(html, 'html.parser')
        listings = []
        seen_urls = set()
        
        for selector, description in selectors:
            logger.info("Trying selector: %s (%s)", selector, description)
            found_items = soup.select(selector)
            
            if found_items:
                logger.info("✓ Found %d items with selector: %s", len(found_items), selector)
                
                for item in found_items:
                    try:
                        title = item.get_text().strip()
                        link = item.get('href', '')
                        
                        # Skip if no title or link
                        if not title or not link or len(title) < 3:
                            continue
                        
                        # Skip duplicates
                        if link in seen_urls:
                            continue
                        
                        # Apply filters if provided
                        if filters:
                            # Title cleanup filter
                            if 'clean_title' in filters:
                                title = filters['clean_title'](title)
                            
                            # Skip filter (e.g., navigation links)
                            if 'skip_filter' in filters and filters['skip_filter'](title, link):
                                continue
                            
                            # Keyword filter
                            if 'keyword_filter' in filters:
                                keyword = filters.get('keyword', '')
                                if keyword and not filters['keyword_filter'](title, keyword):
                                    continue
                            
                            # Prefix filter (e.g., FS:, WTB:)
                            if 'prefix_filter' in filters and not filters['prefix_filter'](title):
                                continue
                        
                        # Build full URL
                        if link.startswith('http'):
                            full_url = link
                        elif link.startswith('/'):
                            full_url = urljoin(base_url, link)
                        else:
                            full_url = urljoin(base_url, link)
                        
                        seen_urls.add(link)
                        
                        listings.append({
                            'title': title,
                            'url': full_url
                        })
                        
                        logger.info("Added: %s", title[:60])
                        
                    except Exception as e:
                        logger.warning("Error processing item: %s", str(e))
                        continue
                
                if listings:
                    break
        
        return listings
    
    def extract_details(self, html, url):
        """
        Extract price and details from individual listing page
        
        Args:
            html: HTML content
            url: URL of the page (for context)
            
        Returns:
            Dict with 'price' and 'details'
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract price
        price = "N/A"
        price_pattern = r'\$[\d,]+(?:\.\d{2})?'
        
        # Look for labeled price
        price_text = soup.find(string=re.compile(r'Price:', re.IGNORECASE))
        if price_text:
            next_text = str(price_text.parent.get_text())
            price_match = re.search(price_pattern, next_text)
            if price_match:
                price = price_match.group()
        
        # Fallback: find any price
        if price == "N/A":
            price_matches = re.findall(price_pattern, html[:5000])
            if price_matches:
                valid_prices = [p for p in price_matches if int(p.replace('$', '').replace(',', '').split('.')[0]) > 50]
                if valid_prices:
                    price = valid_prices[0]
        
        # Extract details
        details = "N/A"
        detail_selectors = [
            "div.post_body",
            "td.alt1[id^='post']",
            "div[id^='post_message']",
            "div.item-description",
            "div.content",
        ]
        
        for selector in detail_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text().strip()
                if len(text) > 100:
                    lines = [line.strip() for line in text.split('\n') if line.strip()]
                    cleaned_lines = [l for l in lines if not any(junk in l.lower() for junk in ['quote', 'edit', 'report'])]
                    details = '\n'.join(cleaned_lines[:15])
                    break
            if details != "N/A":
                break
        
        return {'price': price, 'details': details}
    
    def scrape_with_details(self, urls, delay=2):
        """
        Scrape details from multiple listing URLs
        
        Args:
            urls: List of URLs to scrape
            delay: Delay between requests (seconds)
            
        Returns:
            List of dicts with title, url, price, details
        """
        results = []
        
        for i, listing in enumerate(urls, 1):
            logger.info("Fetching details %d/%d: %s", i, len(urls), listing['url'][:50])
            
            try:
                html = self.fetch_page(listing['url'])
                details = self.extract_details(html, listing['url'])
                
                results.append({
                    'title': listing['title'],
                    'url': listing['url'],
                    'price': details['price'],
                    'details': details['details']
                })
                
                logger.info("Price: %s", details['price'])
                
                if i < len(urls):
                    time.sleep(delay)
                    
            except Exception as e:
                logger.error("Failed to fetch details for %s: %s", listing['url'], str(e))
                results.append({
                    'title': listing['title'],
                    'url': listing['url'],
                    'price': 'N/A',
                    'details': 'Error fetching details'
                })
        
        return results
    
    def close(self):
        """Clean up resources"""
        if self.driver:
            logger.info("Closing browser...")
            self.driver.quit()
            self.driver = None
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


# Scraper Configurations for Different Sites

class FredMirandaScraper(WebScraper):
    """Specialized scraper for Fred Miranda forum"""
    
    def __init__(self):
        super().__init__(scraping_method='selenium')
        self.base_url = "https://www.fredmiranda.com/forum/board/10/"
    
    def scrape_listings(self, search_keyword=None, num_pages=4, max_items=50):
        """
        Scrape Fred Miranda Buy & Sell forum
        
        Args:
            search_keyword: Filter by keyword (e.g., 'sony', 'nikon')
            num_pages: Number of pages to scrape
            max_items: Maximum listings to return
            
        Returns:
            List of listing dictionaries
        """
        all_listings = []
        seen_urls = set()
        
        for page_num in range(num_pages):
            # Build page URL
            if page_num == 0:
                url = self.base_url
            else:
                url = f"{self.base_url}{page_num}/"
            
            logger.info("Scraping page %d: %s", page_num + 1, url)
            
            try:
                html = self.fetch_page(url, wait_time=3)
                
                # Fred Miranda specific selectors
                selectors = [
                    ("tr td a[href*='/forum/topic/']", "Topic links in table cells"),
                    ("a[href*='/forum/topic/']", "Any topic links"),
                ]
                
                # Fred Miranda specific filters
                filters = {
                    'clean_title': lambda t: t.replace(' end', '').strip(),
                    'skip_filter': lambda t, l: t in ['end', '→', '...'] or t.isdigit(),
                    'prefix_filter': lambda t: t.startswith('FS:') or t.startswith('WTB:') or t.startswith('FT:'),
                    'keyword_filter': lambda t, k: k.lower() in t.lower() if k else True,
                    'keyword': search_keyword
                }
                
                page_listings = self.parse_generic_listings(html, self.base_url, selectors, filters)
                
                # Add only new listings
                for listing in page_listings:
                    if listing['url'] not in seen_urls:
                        seen_urls.add(listing['url'])
                        all_listings.append(listing)
                        
                        if len(all_listings) >= max_items:
                            break
                
                logger.info("Page %d: Found %d listings (total: %d)", 
                           page_num + 1, len(page_listings), len(all_listings))
                
                if len(all_listings) >= max_items:
                    break
                    
            except Exception as e:
                logger.error("Error scraping page %d: %s", page_num + 1, str(e))
                continue
        
        return all_listings


class QuotesScraperExample(WebScraper):
    """Example scraper for quotes.toscrape.com (simple site)"""
    
    def __init__(self):
        super().__init__(scraping_method='requests')  # Fast, simple HTTP
        self.base_url = "https://quotes.toscrape.com/"
    
    def scrape_listings(self, max_items=10):
        """Scrape quotes from test site"""
        html = self.fetch_page(self.base_url)
        
        selectors = [("div.quote", "Quote containers")]
        
        soup = BeautifulSoup(html, 'html.parser')
        quotes = []
        
        quote_divs = soup.select("div.quote")
        for idx, quote_div in enumerate(quote_divs[:max_items]):
            quote_text = quote_div.select_one("span.text")
            author = quote_div.select_one("small.author")
            
            if quote_text and author:
                quotes.append({
                    'title': f"{quote_text.get_text()[:50]}... - {author.get_text()}",
                    'url': f"{self.base_url}#quote-{idx}",
                    'price': 'N/A',
                    'details': quote_text.get_text()
                })
        
        return quotes


def save_results(listings, filename="scraped_listings.txt"):
    """Save results to file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Web Scraper Results - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            for i, item in enumerate(listings, 1):
                f.write(f"ITEM #{i}\n")
                f.write(f"Title: {item['title']}\n")
                f.write(f"Price: {item.get('price', 'N/A')}\n")
                f.write(f"URL: {item['url']}\n")
                if 'details' in item:
                    details = item['details'][:200] if len(item['details']) > 200 else item['details']
                    f.write(f"Details: {details}\n")
                f.write("-" * 80 + "\n\n")
        
        logger.info("Results saved to %s", filename)
        return True
    except Exception as e:
        logger.error("Failed to save results: %s", str(e))
        return False


# Main CLI interface
if __name__ == "__main__":
    print("=" * 60)
    print("Universal Web Scraper")
    print("=" * 60)
    print()
    print("Select scraper type:")
    print("1. Fred Miranda Buy & Sell (Selenium - requires Safari setup)")
    print("2. Quotes Test Site (Simple HTTP - no setup needed)")
    print()
    
    choice = input("Enter choice (1-2): ").strip()
    
    if choice == "1":
        # Fred Miranda scraper
        if not SELENIUM_AVAILABLE:
            print("\nError: Selenium not installed!")
            print("Install with: pip3 install selenium")
            exit(1)
        
        print("\nSafari Setup Required:")
        print("1. Safari > Settings > Advanced")
        print("2. Check 'Show Develop menu'")
        print("3. Develop > Allow Remote Automation")
        input("\nPress Enter when ready...")
        
        search_keyword = input("\nEnter search keyword (or Enter for all): ").strip() or None
        
        with FredMirandaScraper() as scraper:
            print(f"\nScraping Fred Miranda for '{search_keyword or 'ALL'}' listings...")
            listings = scraper.scrape_listings(search_keyword=search_keyword, num_pages=4, max_items=50)
            
            if listings:
                print(f"\n✓ Found {len(listings)} listings!")
                
                # Get details
                print("\nFetching prices and details...")
                full_results = scraper.scrape_with_details(listings, delay=2)
                
                # Save and display
                filename = f"fred_miranda_{search_keyword or 'all'}_listings.txt"
                save_results(full_results, filename)
                
                print("\n" + "=" * 60)
                print("RESULTS:")
                print("=" * 60)
                for i, item in enumerate(full_results[:5], 1):
                    print(f"\n[{i}] {item['title']}")
                    print(f"    Price: {item['price']}")
                    print(f"    URL: {item['url']}")
                
                if len(full_results) > 5:
                    print(f"\n... and {len(full_results) - 5} more (see {filename})")
            else:
                print("\n✗ No listings found")
    
    elif choice == "2":
        # Simple test scraper
        with QuotesScraperExample() as scraper:
            print("\nScraping quotes test site...")
            quotes = scraper.scrape_listings(max_items=10)
            
            if quotes:
                print(f"\n✓ Found {len(quotes)} quotes!")
                save_results(quotes, "quotes_test.txt")
                
                for i, quote in enumerate(quotes[:5], 1):
                    print(f"\n[{i}] {quote['title']}")
            else:
                print("\n✗ No quotes found")
    
    else:
        print("\nInvalid choice!")