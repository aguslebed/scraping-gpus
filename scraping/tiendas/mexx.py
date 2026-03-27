from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from datetime import datetime
from .baseScrapingClass import BaseScraper
from Gpu import Gpu
from utils import find_chipset, clean_price

class Mexx(BaseScraper):
    def __init__(self, headers, base_url):
        super().__init__(headers, base_url)
        self.raw_html_list = []
        self.parsed_data = []
        self.scraped_products = []

    def fetch(self):
        print(f"Fetching {self.base_url}...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(extra_http_headers=self.headers)
            page.goto(self.base_url, wait_until="domcontentloaded")
            page.wait_for_timeout(2000) # give it some time to render JS
            

            page_num = 2
            
            while True:
                # Get the HTML of the current page
                html = page.content()
                self.raw_html_list.append(html)
                
                # Check if the next page button exists by looking for the page number text in the pagination list
                try:
                    next_page_locator = page.locator(f'ul.pagination a:has-text("{page_num}")').first
                    next_page_locator.wait_for(state="attached", timeout=3000)
                    
                    if next_page_locator.count() > 0:
                        page.evaluate(f"enviarPagina({page_num})")
                        # wait for page reload / ajax
                        page.wait_for_timeout(3000)
                        page_num += 1
                    else:
                        break
                except:
                    break

            browser.close()

    def parse(self):
        print(f"Parsing html...")
        for raw_html in self.raw_html_list:
            soup = BeautifulSoup(raw_html, 'html.parser')
            # Mexx products are contained in divs with this class structure
            products_in_page = soup.select('div.card.card-ecommerce')
            self.parsed_data.extend(products_in_page)

        print(f"Parsed {len(self.parsed_data)} products containers")

    def extract_products(self):
        for product in self.parsed_data:
            # Name and URL
            title_element = product.select_one('h4.card-title a')
            if not title_element:
                continue
            
            name = title_element.text.strip()
            
            # The user requested that we ensure ALL items effectively start with 'Placa De Video' to be pure GPUs
            if not name.lower().startswith('placa de video'):
                continue
                
            url = title_element.get('href', '')
            if url and url.startswith('/'):
                # Handle relative urls if encountered
                url = 'https://www.mexx.com.ar' + url

            # Price
            price_container = product.select_one('div.price h4 b')
            if price_container:
                price_text = price_container.text.strip()
                price = clean_price(price_text)
            else:
                price = 0

            # Image
            img_container = product.select_one('div.view img')
            image_url = img_container.get('src') if img_container else ""

            # Outlet property
            outlet = "usada" in name.lower() or "outlet" in name.lower()

            chipset = find_chipset(name)

            date = datetime.now()

            gpu = Gpu(name, chipset, price, url, image_url, outlet, "Mexx", date)
            self.scraped_products.append(gpu.get_obj())
        print(f"Extracted {len(self.scraped_products)} products")

    def scrape(self, url=None):
        self.fetch()
        self.parse()
        self.extract_products()
        return self.scraped_products

