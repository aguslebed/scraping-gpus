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
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded")
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
        return html.find_all('article', class_=lambda x: x and 'mxCardProduct' in x)

    def extract_products(self, parsed):
        products = []
        for product in parsed:
            try:
                ################### NOMBRE ###################
                name_tag = product.find('h3', class_='mxCardProduct__title')
                if not name_tag:
                    continue
                
                name = name_tag.text.strip()
                if name.lower().startswith("placa de video") == False:
                    continue

                ################### IMAGEN ###################
                img_url = ""
                img_container = product.find('div', class_='mxCardProduct__imageBox')
                if img_container:
                    img_tag = img_container.find('img')
                    if img_tag:
                        img_url = img_tag.get('src') or img_tag.get('data-src') or ""
                
                ################### PRECIO ###################
                price_tag = product.find('div', class_='mxCardProduct__price')
                if not price_tag:
                    continue
                price = int(clean_price(price_tag.text))
                
                ################### URL ###################
                link_tag = product.find('a', class_='mxCardProduct__link')
                if not link_tag:
                    continue
                url = link_tag.get('href')
                final_url = url if url.startswith('http') else f"{self.base_url}{url}"
                
                ################### CHIPSET ###################
                chipset = find_chipset(name)
                
                ################### FECHA ###################
                date = datetime.now()
                
                ################### GPU ###################
                gpu = Gpu(name,chipset, price, final_url, img_url, False, 'Maximus', date)
                
                ################### OUTLET ###################
                div_outlet = product.find('div', class_=lambda x: x and 'mxCardProduct__badge' in x and 'outlet' in x.lower())
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