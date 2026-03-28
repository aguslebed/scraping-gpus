import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scraping'))

from playwright.sync_api import sync_playwright

def test():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3' 
    }
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(extra_http_headers=headers)
        page.goto('https://www.libreopcion.com/placas-de-video', wait_until="networkidle")
        page.wait_for_timeout(2000)
        
        with open('lo_playwright_test.html', 'w', encoding='utf-8') as f:
            f.write(page.content())
        browser.close()

if __name__ == '__main__':
    test()
