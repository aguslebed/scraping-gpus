from baseScrapingClass import BaseScraper
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from Gpu import Gpu
from utils import find_chipset, clean_price
from datetime import datetime

class CompraGamer(BaseScraper):

    def __init__(self, headers, base_url):
        super().__init__(headers, base_url)

    def fetch(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")
            page.get_by_placeholder("Buscá por productos, marcas y categorías").fill("placa de video")
            page.get_by_placeholder("Buscá por productos, marcas y categorías").press("Enter")
            page.wait_for_timeout(2000) 
            
            # Scroll down slowly to trigger lazy-loaded images
            for i in range(5):
                page.evaluate("window.scrollBy(0, 1000)")
                page.wait_for_timeout(500)
            
            soup = BeautifulSoup(page.content(), 'html.parser')
        return soup

    def parse(self, html):
        return html.findAll('a', class_='product-card cg__primary-card medium vertical responsive notSelected')

    def extract_products(self, parsed):
        products = []
        for product in parsed:
            try:
                name_tag = product.find('h3', class_='product-card__title cg__fw-400 mb-2 ng-star-inserted')
                if not name_tag:
                    continue
                
                # Usamos .strip() para limpiar espacios al principio y al final
                name = name_tag.text.strip()
                if name.startswith("Placa de Video") == False:
                    continue

                img_tag = product.find('img')
                img_url = ""
                if img_tag and img_tag.has_attr('src'):
                    img_url = img_tag['src']
                elif img_tag and img_tag.has_attr('data-src'):
                    img_url = img_tag['data-src']
                
                
                
                price_tag = product.find('span', class_='txt_price')
                if not price_tag:
                    continue
                price = clean_price(price_tag.text)
                
                url = product.get('href')
                final_url = f"{self.base_url}{url}"
                chipset = find_chipset(name)
                date = datetime.now()
                gpu = Gpu(name,chipset, price, final_url, img_url, False, 'Compra Gamer', date)
                products.append(gpu.get_obj())    
            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f"Error al extraer el producto: {e}")
        
        return products
            

    def scrape(self):
        print("Fetching html...")
        html = self.fetch(self.base_url)
        print("Parsing html...")
        parsed = self.parse(html)
        print(f"Parsed {len(parsed)} products")
        products = self.extract_products(parsed)
        print(f"Extracted {len(products)} products")
        return products