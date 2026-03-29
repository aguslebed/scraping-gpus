import sys, os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from baseScrapingClass import BaseScraper
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
from datetime import datetime
from Gpu import Gpu
from utils import find_chipset, clean_price

class QuantumHardStore(BaseScraper):
    def __init__(self, headers, base_url):
        super().__init__(headers, base_url)
        self.raw_html_list = []
        self.parsed_data = [] # Para items de json
        self.scraped_products = []

    def fetch(self):
        print(f"Fetching {self.base_url}...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(extra_http_headers=self.headers)
            
            try:
                print(f"Loading {self.base_url}...")
                page.goto(self.base_url, wait_until="domcontentloaded")
                # Tiene una carga la primera vez, damos tiempo para que termine
                page.wait_for_timeout(5000) 
                
                # Scrolleamos hasta abajo suavemente para gatillar imagenes y posible lazy load
                page.evaluate("""
                    window.scrollTo(0, document.body.scrollHeight);
                """)
                page.wait_for_timeout(2000)
                
                html = page.content()
                self.raw_html_list.append(html)
            except Exception as e:
                print(f"Error fetching QuantumHardStore page: {e}")
                
            browser.close()

    def parse(self):
        print(f"Parsing html...")
        for raw_html in self.raw_html_list:
            soup = BeautifulSoup(raw_html, 'html.parser')
            # Extraemos los scripts con json de schema.org para sacar name, price, img, url
            scripts = soup.select('script[data-component="structured-data.item"]')
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    if data.get("@type") == "Product":
                        self.parsed_data.append(data)
                except Exception:
                    pass

        print(f"Parsed {len(self.parsed_data)} products JSON structures")

    def extract_products(self):
        # Para evitar duplicados leyendo el html
        vistos = set()
        
        for data in self.parsed_data:
            try:
                name = data.get("name", "")
                if not name:
                    continue
                    
                name_lower = name.lower()
                
                # Nos aseguramos de saltar cosas raras, o no.
                # Ya sabemos que estamos en la categoria placas de video.
                
                url = ""
                price_text = ""
                offers = data.get("offers", {})
                
                if isinstance(offers, list) and len(offers) > 0:
                    offers = offers[0]
                    
                url = offers.get("url", "")
                price_text = offers.get("price", "0")
                
                if not url or url in vistos:
                    continue
                vistos.add(url)
                    
                price = int(float(price_text)) if price_text else 0
                
                # Si el precio es 0 puede ser un producto sin stock, lo sumamos igual si la logica lo prevee
                
                image_url = data.get("image", "")
                
                outlet = "usada" in name_lower or "outlet" in name_lower
                chipset = find_chipset(name)
                date = datetime.now()

                gpu = Gpu(name, chipset, price, url, image_url, outlet, "QuantumHardStore", date)
                self.scraped_products.append(gpu.get_obj())
                
            except Exception as e:
                print(f"Error extracting product in QuantumHardStore: {e}")
                
        print(f"Extracted {len(self.scraped_products)} products")

    def scrape(self):
        self.fetch()
        self.parse()
        self.extract_products()
        return self.scraped_products
