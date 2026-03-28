import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .baseScrapingClass import BaseScraper
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from Gpu import Gpu
from utils import find_chipset, clean_price
from datetime import datetime

class LibreOpcion(BaseScraper):
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
            page.goto(self.base_url, wait_until="networkidle")
            page.wait_for_timeout(2000)

            previous_scroll = -1
            unchanged_scroll_count = 0
            max_scrolls = 150
            scroll_count = 0

            while scroll_count < max_scrolls:
                scroll_count += 1
                
                # Scrolleamos paso a paso en vez de ir directo al fondo para que las publicaciones vayan apareciendo
                page.evaluate("window.scrollBy(0, 1000)")
                page.wait_for_timeout(1000)
                
                # Chequeamos el progreso
                current_scroll = page.evaluate("window.scrollY")
                total_height = page.evaluate("document.body.scrollHeight")
                
                if current_scroll == previous_scroll:
                    unchanged_scroll_count += 1
                else:
                    unchanged_scroll_count = 0
                
                previous_scroll = current_scroll
                
                bottom_reached = page.evaluate("window.scrollY + window.innerHeight") >= total_height - 100
                
                if bottom_reached or unchanged_scroll_count >= 3:
                    # Esperamos la respuesta de la web para cargar los nuevos productos
                    page.wait_for_timeout(2500)
                    new_total_height = page.evaluate("document.body.scrollHeight")
                    
                    if new_total_height == total_height:
                        break # Ya cargó todo el infinito, podemos salir
                    else:
                        unchanged_scroll_count = 0
                        
            self.raw_html_list.append(page.content())
            browser.close()

    def parse(self):
        print(f"Parsing html...")
        for raw_html in self.raw_html_list:
            soup = BeautifulSoup(raw_html, 'html.parser')
            # Los productos estan en a.productos-modulo-c o div.productos-modulo-c ... o modulo-b
            products = soup.select('div.productos-modulo-c')
            if not products:
                products = soup.select('a.productos-modulo-c')
            if not products:
                products = soup.select('div.productos-modulo-b')
            if not products:
                products = soup.select('a.productos-modulo-b')
                
            self.parsed_data.extend(products)

        print(f"Parsed {len(self.parsed_data)} products containers")

    def extract_products(self):
        for product in self.parsed_data:
            try:
                # Titulo
                title_elem = product.select_one('h2.description')
                if not title_elem:
                    continue
                name = title_elem.text.strip().replace('\n', '')

                # Validar que sea GPU
                name_lower = name.lower()
                if 'placa de video' not in name_lower and 'rtx' not in name_lower and 'rx' not in name_lower and 'gtx' not in name_lower:
                    continue

                # URL
                url = ""
                if product.name == 'a':
                    url = product.get('href', '')
                else:
                    a_elem = product.select_one('a')
                    if a_elem:
                        url = a_elem.get('href', '')
                        
                if url and url.startswith('/'):
                    url = 'https://www.libreopcion.com' + url

                # Precio
                price_elem = product.select_one('div.price-final p')
                price = 0
                if price_elem:
                    # Removemos el tag <i> que contiene los centavos
                    i_tag = price_elem.select_one('i')
                    if i_tag:
                        i_tag.decompose()
                    
                    price_text = price_elem.text.strip()
                    try:
                        price = int(clean_price(price_text).strip())
                    except ValueError:
                        price = 0

                if price == 0:
                    continue

                # Imagen
                img_elem = product.select_one('div.imagen img')
                img_url = ""
                if img_elem:
                    img_url = img_elem.get('src') or img_elem.get('data-src') or ""

                # Outlet
                is_outlet = 'usada' in name_lower or 'outlet' in name_lower 

                # Chipset
                chipset = find_chipset(name)

                # Fecha
                date = datetime.now()

                gpu = Gpu(name, chipset, price, url, img_url, is_outlet, 'LibreOpcion', date)
                self.scraped_products.append(gpu.get_obj())

            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f"Error al extraer el producto: {e}")

        print(f"Extracted {len(self.scraped_products)} products")

    def scrape(self, url=None):
        self.fetch()
        self.parse()
        self.extract_products()
        return self.scraped_products


