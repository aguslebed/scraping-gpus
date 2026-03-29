from requests import head
from baseScrapingClass import BaseScraper
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from Gpu import Gpu
from utils import find_chipset, clean_price
from datetime import datetime

class Maximus(BaseScraper):

    def __init__(self, headers, base_url):
        super().__init__(headers, base_url)

    def fetch(self, url):
        combined_html = ""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")
            page.get_by_placeholder("Buscar en Maximus").fill("placa de video")
            page.get_by_placeholder("Buscar en Maximus").press("Enter")
            page.wait_for_timeout(2000) 
            
            while True:
                # Scroll down slowly to trigger lazy-loaded images
                for i in range(5):
                    page.evaluate("window.scrollBy(0, 1000)")
                    page.wait_for_timeout(500)
                
                combined_html += page.content()
                
                current_url = page.url
                next_btn = page.locator("img[alt='Próximo']")
                if next_btn.is_visible():
                    next_btn.click()
                    page.wait_for_timeout(2000)
                    if page.url == current_url:
                        break
                else:
                    break
                    
        return BeautifulSoup(combined_html, 'html.parser')

    def parse(self, html):
        return html.find_all('div', class_='product')

    def extract_products(self, parsed):
        products = []
        for product in parsed:
            try:
                ################### NOMBRE ###################
                name_tag = product.find('span', class_='title-prod')
                if not name_tag:
                    continue
                
                name = name_tag.text.strip()
                if name.startswith("Placa de Video") == False:
                    continue

                ################### IMAGEN ###################
                img_url = ""
                img_container = product.find('div', class_='image')
                if img_container:
                    img_tag = img_container.find('img')
                    if img_tag:
                        img_url = img_tag.get('src') or img_tag.get('data-src') or ""
                
                ################### PRECIO ###################
                price_tag = product.find('div', class_='price')
                if not price_tag:
                    continue
                price = int(clean_price(price_tag.text))
                
                ################### URL ###################
                url = product.find('a').get('href')
                final_url = url if url.startswith('http') else f"{self.base_url}{url}"
                
                ################### CHIPSET ###################
                chipset = find_chipset(name)
                
                ################### FECHA ###################
                date = datetime.now()
                
                ################### GPU ###################
                gpu = Gpu(name,chipset, price, final_url, img_url, False, 'Maximus', date)
                
                ################### OUTLET ###################
                div_outlet = product.find('div', class_='product-card__badge')
                if div_outlet:
                    gpu.is_outlet = True

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