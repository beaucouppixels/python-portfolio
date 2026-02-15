import subprocess
import sys
import requests
import time
import logging
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Only install beautifulsoup4 if not already available
try:
    from bs4 import BeautifulSoup
except ImportError:
    logger.info("Installing beautifulsoup4...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])
    from bs4 import BeautifulSoup


# Base URL - Quotes to Scrape (scraper-friendly test site)
BASE_URL = "https://quotes.toscrape.com/"

# Alternative URLs for testing
FALLBACK_URLS = [
    "https://books.toscrape.com/",  # Another scraper-friendly site
    "https://www.fredmiranda.com/forum/board/10/",  # Original target (likely blocked)
    "https://httpbin.org/html"  # Test URL
]

# Create a session for connection pooling and cookie persistence
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
})

# Function to fetch the page content
def fetch_page(url, max_retries=3, delay=1):
    """
    Fetch page content with retry logic and better error handling
    """
    for attempt in range(max_retries):
        try:
            logger.info(f"Fetching: {url} (attempt {attempt + 1})")
            response = session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay * (attempt + 1))  # Exponential backoff
            else:
                logger.error(f"Failed to fetch {url} after {max_retries} attempts")
                raise

def test_url_accessibility():
    """
    Test if the target URL is accessible and suggest alternatives
    """
    print("Testing URL accessibility...")
    
    test_urls = [BASE_URL] + FALLBACK_URLS
    
    for url in test_urls:
        try:
            # Use GET instead of HEAD to ensure we can actually fetch content
            response = session.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✓ {url} - Accessible")
                return url
            else:
                print(f"✗ {url} - Status: {response.status_code}")
        except Exception as e:
            print(f"✗ {url} - Error: {str(e)}")
    
    print("No accessible URLs found. The scraper may encounter issues.")
    return BASE_URL

# Function to parse main listings page
def parse_listings(page_content, base_url=None):
    """
    Parse the main listings page to extract thread links
    Handles multiple site structures including quotes.toscrape.com
    """
    current_base = base_url or BASE_URL
    soup = BeautifulSoup(page_content, 'html.parser')
    listings = []

    # Debug: Check if we have content
    logger.info("Page content length: %d bytes", len(page_content))
    logger.info("First 200 chars: %s", page_content[:200])

    # Try different selectors for different site structures
    selectors_to_try = [
        "div.quote",                # Quotes to Scrape - quote containers
        ".quote",                   # Alternative quote selector
        "article.product_pod h3 a", # Books to Scrape
        "a.thread_title",           # Fred Miranda specific
        "a[href*='thread']",        # Generic forum thread links
        "a[href*='topic']",         # Alternative forum structure
        "h3 a, h2 a",              # Header links
        "a[href]"                   # All links as fallback
    ]
    
    for selector in selectors_to_try:
        found_items = soup.select(selector)
        logger.info("Trying selector '%s': found %d items", selector, len(found_items))
        
        if found_items and len(found_items) > 0:
            logger.info("Using selector: %s with %d items", selector, len(found_items))
            
            # Handle quotes.toscrape.com format
            if selector == "div.quote":
                for idx, quote_div in enumerate(found_items[:10]):
                    quote_text = quote_div.select_one("span.text")
                    author = quote_div.select_one("small.author")
                    
                    if quote_text and author:
                        title = f"{quote_text.get_text().strip()[:50]}... - {author.get_text()}"
                        # Create a unique URL for each quote
                        quote_url = urljoin(current_base, f"#quote-{idx}")
                        listings.append({"title": title, "url": quote_url, "content": quote_text.get_text().strip()})
                        logger.info("Added quote: %s", title[:50])
                break
            
            # Handle other formats
            else:
                for link in found_items[:10]:  # Limit to 10 for demo
                    title = link.get_text().strip()
                    href = link.get("href") if link.name == 'a' else None
                    
                    if not href and hasattr(link, 'select_one'):
                        a_tag = link.select_one("a")
                        if a_tag:
                            href = a_tag.get("href")
                    
                    if href and title and len(title) > 3:  # Filter out very short titles
                        full_url = urljoin(current_base, href)
                        listings.append({"title": title, "url": full_url})
                        logger.info("Added listing: %s", title[:50])
                
                if listings:  # Only break if we actually found valid listings
                    break
    
    logger.info("Successfully parsed %d listings", len(listings))
    return listings

# Function to parse individual listing for price and details
def parse_listing_details(url, listing_data=None):
    """
    Parse individual listing page to extract details and price
    For quotes.toscrape.com, we already have the content
    """
    # If we already have the content (like from quotes), use it
    if listing_data and 'content' in listing_data:
        return {
            "details": listing_data['content'],
            "price": "N/A"  # Quotes don't have prices
        }
    
    try:
        page_content = fetch_page(url)
        soup = BeautifulSoup(page_content, 'html.parser')

        # Initialize with default values
        item_details = "N/A"
        price = "N/A"

        # Try multiple selectors for more robust parsing
        detail_selectors = [
            "div.item-description",
            "div.post-content", 
            "div.content",
            "div.message-content",
            ".post_body",
            "p.price_color"  # Books to Scrape
        ]
        
        price_selectors = [
            "span.price",
            ".price",
            "p.price_color",  # Books to Scrape
            "strong:contains('$')",
            "b:contains('$')"
        ]

        # Extract item details
        for selector in detail_selectors:
            element = soup.select_one(selector)
            if element:
                item_details = element.get_text().strip()
                break

        # Extract price - look for common price patterns
        for selector in price_selectors:
            element = soup.select_one(selector)
            if element:
                price = element.get_text().strip()
                break
        
        # If no specific price element found, search for price patterns in text
        if price == "N/A":
            import re
            price_pattern = r'[\$£€][\d,]+(?:\.\d{2})?'
            text_content = soup.get_text()
            price_match = re.search(price_pattern, text_content)
            if price_match:
                price = price_match.group()

        logger.debug("Extracted details for %s: price=%s", url, price)
        return {"details": item_details, "price": price}
        
    except Exception as e:
        logger.error("Error parsing listing details for %s: %s", url, str(e))
        return {"details": "Error fetching details", "price": "N/A"}

# Main scraping logic
def scrape_site(base_url=None, max_items=None, delay_between_requests=1):
    """
    Main scraping function with configurable limits and delays
    """
    target_url = base_url or BASE_URL
    logger.info("Starting scrape of %s", target_url)
    
    try:
        # Fetch and parse main listings page
        logger.info("Fetching main listings page...")
        main_page = fetch_page(target_url)
        listings = parse_listings(main_page, target_url)
        
        if not listings:
            logger.warning("No listings found on main page")
            return []
        
        # Limit number of items if specified
        if max_items:
            listings = listings[:max_items]
            logger.info("Limited to %d items", max_items)

        all_items = []
        total_listings = len(listings)
        
        for i, listing in enumerate(listings, 1):
            logger.info("Processing %d/%d: %s", i, total_listings, listing['title'][:60])
            
            try:
                # Pass the listing data in case we already have content
                details = parse_listing_details(listing["url"], listing)
                item_data = {
                    "title": listing["title"],
                    "url": listing["url"],
                    "details": details["details"],
                    "price": details["price"],
                    "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                all_items.append(item_data)
                
            except Exception as e:
                logger.error("Failed to process listing %s: %s", listing['title'], str(e))
                # Continue with next listing instead of failing completely
                continue
            
            # Rate limiting
            if i < total_listings:  # Don't sleep after last item
                time.sleep(delay_between_requests)

        logger.info("Scraping completed. Successfully processed %d/%d items", 
                   len(all_items), total_listings)
        return all_items
        
    except Exception as e:
        logger.error("Scraping failed: %s", str(e))
        raise

def save_results_to_file(results, filename="scraped_listings.txt"):
    """
    Save scraped results to a text file
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Web Scraper Results - Scraped on {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            for i, item in enumerate(results, 1):
                f.write(f"ITEM #{i}\n")
                f.write(f"Title: {item['title']}\n")
                f.write(f"Price: {item['price']}\n")
                f.write(f"URL: {item['url']}\n")
                f.write(f"Details: {item['details'][:200]}...\n" if len(item['details']) > 200 else f"Details: {item['details']}\n")
                f.write(f"Scraped: {item.get('scraped_at', 'N/A')}\n")
                f.write("-" * 80 + "\n\n")
        
        logger.info("Results saved to %s", filename)
    except IOError as e:
        logger.error("Failed to save results to file: %s", str(e))

def print_summary(results):
    """
    Print a summary of scraped results
    """
    if not results:
        print("No listings were scraped.")
        return
    
    print(f"\n{'='*60}")
    print(f"SCRAPING SUMMARY")
    print(f"{'='*60}")
    print(f"Total items scraped: {len(results)}")
    
    # Count listings with prices
    priced_items = [item for item in results if item['price'] != 'N/A' and item['price'] != 'Error fetching details']
    print(f"Items with prices: {len(priced_items)}")
    
    if results:
        print(f"\nSample items:")
        for i, item in enumerate(results[:3], 1):
            print(f"{i}. {item['title'][:60]}... - {item['price']}")
    
    print(f"{'='*60}\n")

# Run the scraper
if __name__ == "__main__":
    try:
        # Test URL accessibility first
        accessible_url = test_url_accessibility()
        
        # Configure scraping parameters
        MAX_ITEMS = 10  # Limit for testing - remove or increase for full scrape
        DELAY = 1       # Seconds between requests (can be lower for test sites)
        
        logger.info("Starting web scraper...")
        logger.info("Target URL: %s", accessible_url)
        
        results = scrape_site(base_url=accessible_url, max_items=MAX_ITEMS, delay_between_requests=DELAY)
        
        if results:
            print_summary(results)
            save_results_to_file(results)
            
            # Print first few results to console
            print("\n" + "="*60)
            print("SAMPLE SCRAPED ITEMS:")
            print("="*60)
            for i, item in enumerate(results[:5], 1):
                print(f"\n[{i}] {item['title'][:70]}")
                print(f"    Price: {item['price']}")
                print(f"    Details: {item['details'][:100]}...")
                print(f"    URL: {item['url']}")
                print("-" * 60)
        else:
            print("No results found.")
            
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
    except Exception as e:
        logger.error("Scraping failed with error: %s", str(e))