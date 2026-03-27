import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from baseScrapingClass import BaseScraper
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
from datetime import datetime
from Gpu import Gpu
from utils import find_chipset, clean_price

class FullH4rd(BaseScraper):
    def __init__(self, headers, base_url):
        super().__init__(headers, base_url)

    def fetch(self, url):
        self.raw_html_list = []
        # Para FullHard usamos paginacion, asique empezamos desde la pagina 1
        start_url = f"{self.base_url}/cat/supra/3/placas-de-video/1/menor"
        print(f"Fetching {start_url}... ")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            try:
                page.goto(start_url)
                
                # Cloudflare check / wait for products to load
                page.wait_for_selector('div.item.product-list', timeout=15000)
                
                while True:
                    # Scroll down to ensure dynamic elements load
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1.5)
                    
                    self.raw_html_list.append(page.content())
                    
                    # Look for the 'Siguiente' button in pagination
                    next_button = page.locator('div.paginator.air a[rel="next"]')
                    
                    if next_button.count() > 0:
                        next_url = next_button.first.get_attribute("href")
                        if next_url:
                            full_next_url = f"{self.base_url.rstrip('/')}{next_url}"
                            print(f"Navigating to next page: {full_next_url}")
                            page.goto(full_next_url)
                            page.wait_for_selector('div.item.product-list', timeout=15000)
                        else:
                            break
                    else:
                        break # No Siguiente button found

            except Exception as e:
                print(f"Error fetching from {self.base_url}: {e}")
            finally:
                browser.close()
                return self.raw_html_list

    def parse(self, html_list):
        all_products = []
        for html in html_list:
            soup = BeautifulSoup(html, 'html.parser')
            products = soup.find_all('div', class_='item product-list')
            all_products.extend(products)
        return all_products

    def extract_products(self, parsed):
        extracted_gpus = []
        for product in parsed:
            try:
                # Name
                name_tag = product.find('h3')
                if not name_tag:
                    continue
                name = name_tag.text.strip()
                
                name_lower = name.lower()
                if 'placa' not in name_lower and 'video' not in name_lower and 'vga' not in name_lower and 'geforce' not in name_lower and 'radeon' not in name_lower:
                    continue

                # URL
                a_tag = product.find('a')
                if not a_tag:
                    continue
                url_product = a_tag.get('href', '')
                if not url_product.startswith('http'):
                    url_product = f"{self.base_url.rstrip('/')}{url_product}"
                
                # Image
                image_tag = product.find('div', class_='image')
                image_url = ""
                if image_tag:
                    img = image_tag.find('img')
                    if img:
                        image_url = img.get('src', '')
                        if not image_url.startswith('http'):
                            image_url = f"{self.base_url.rstrip('/')}{image_url}"

                # Price
                price_div = product.find('div', class_='price')
                if not price_div:
                    continue
                
                span_promo = price_div.find('span', class_='price-promo')
                if span_promo:
                    span_promo.extract()
                    
                price_text = price_div.text.strip().split(',')[0]
                price = int(clean_price(price_text))
                
                # Outlet
                is_outlet = 'outlet' in name_lower or 'usada' in name_lower
                
                # Chipset
                chipset = find_chipset(name)
                
                # Date
                date = datetime.now()
                
                gpu = Gpu(name, chipset, price, url_product, image_url, is_outlet, "FullH4rd", date)
                extracted_gpus.append(gpu.get_obj())
            
            except Exception as e:
                print(f"Error parsing product in FullH4rd: {e}")
                
        return extracted_gpus

    def scrape(self):
        print("Fetching html...")
        html_list = self.fetch(self.base_url)
        if not html_list:
            return []
        print("Parsing html...")
        parsed = self.parse(html_list)
        print(f"Parsed {len(parsed)} products containers")
        products = self.extract_products(parsed)
        print(f"Extracted {len(products)} products")
        return products
