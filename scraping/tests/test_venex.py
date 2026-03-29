import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'tiendas'))
from tiendas.venex import Venex

def test_venex():
    print("Testing Venex scraper...")
    scraper = Venex({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    })
    
    results = scraper.scrape()
    print(f"Ended testing. Results: {len(results)}")
    
    # Print the first 5 results to check
    for r in results[:5]:
        print(r)

if __name__ == "__main__":
    test_venex()
