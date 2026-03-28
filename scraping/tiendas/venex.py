import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from baseScrapingClass import BaseScraper
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
from datetime import datetime
from Gpu import Gpu
from utils import find_chipset, clean_price

class Venex(BaseScraper):
    def __init__(self, headers, base_url="https://www.venex.com.ar/componentes-de-pc/placas-de-video"):
        super().__init__(headers, base_url)
        self.raw_html_list = []
        self.parsed_data = []
        self.scraped_products = []

    def fetch(self):
        print(f"Fetching {self.base_url}...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(extra_http_headers=self.headers)
            
            page_num = 1
            while True:
                # Venex pagination pattern
                if page_num == 1:
                    current_url = f"{self.base_url}?vmm=12" # adding ?vmm=12 like the original url
                else:
                    current_url = f"{self.base_url}?vmm=12&page={page_num}"
                
                try:
                    print(f"Loading {current_url}...")
                    page.goto(current_url, wait_until="domcontentloaded")
                    page.wait_for_timeout(2000) # give it a moment to load
                    
                    html = page.content()
                    self.raw_html_list.append(html)
                    
                    # Verify if there's a next page or if products are empty
                    soup = BeautifulSoup(html, 'html.parser')
                    products = soup.select('div.product-box')
                    if not products:
                        print(f"No products found on page {page_num}. Ending pagination.")
                        break
                    
                    # Also check for pagination explicitly 
                    page_links = soup.select('ul.pagination a')
                    has_next = False
                    for link in page_links:
                        title_text = link.get('title', '')
                        if 'Siguiente' in title_text or 'Siguientes' in title_text or 'fa-chevron-right' in str(link):
                            has_next = True
                            break
                        # O si existe el link a la página actual + 1
                        if link.text.strip() == str(page_num + 1):
                            has_next = True
                            break
                    
                    if not has_next:
                        print(f"No more pages after page {page_num}.")
                        break
                    
                    page_num += 1
                except Exception as e:
                    print(f"Error fetching Venex page {page_num}: {e}")
                    break
                    
            browser.close()

    def parse(self):
        print(f"Parsing html...")
        for raw_html in self.raw_html_list:
            soup = BeautifulSoup(raw_html, 'html.parser')
            # Los productos estan en div.product-box
            products = soup.select('div.product-box')
            self.parsed_data.extend(products)

        print(f"Parsed {len(self.parsed_data)} products containers")

    def extract_products(self):
        for product in self.parsed_data:
            try:
                # Name and URL
                title_elem = product.select_one('h3.product-box-title a')
                if not title_elem:
                    continue
                
                name = title_elem.text.strip()
                name_lower = name.lower()
                
                # Check for video card
                if 'placa' not in name_lower and 'video' not in name_lower and 'vga' not in name_lower and 'geforce' not in name_lower and 'radeon' not in name_lower:
                    continue

                url = title_elem.get('href', '')
                if url and not url.startswith('http'):
                    url = 'https://www.venex.com.ar' + url

                # Price
                price_container = product.select_one('span.current-price')
                if price_container:
                    price_text = price_container.text.strip()
                    price = clean_price(price_text)
                else:
                    price = 0

                # Image
                img_elem = product.select_one('div.thumb img')
                if not img_elem:
                    img_elem = product.select_one('div.product-box-media img')
                    
                image_url = ""
                if img_elem:
                    image_url = img_elem.get('src', '')
                    if image_url and not image_url.startswith('http'):
                        image_url = 'https://www.venex.com.ar/' + image_url.lstrip('/')

                # Outlet check
                outlet = "usada" in name_lower or "outlet" in name_lower

                chipset = find_chipset(name)
                date = datetime.now()

                gpu = Gpu(name, chipset, price, url, image_url, outlet, "Venex", date)
                self.scraped_products.append(gpu.get_obj())
                
            except Exception as e:
                print(f"Error extracting product in Venex: {e}")
                
        print(f"Extracted {len(self.scraped_products)} products")

    def scrape(self):
        self.fetch()
        self.parse()
        self.extract_products()
        return self.scraped_products
