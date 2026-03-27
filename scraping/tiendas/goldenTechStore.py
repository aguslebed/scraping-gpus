import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from baseScrapingClass import BaseScraper
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from Gpu import Gpu
from utils import find_chipset, clean_price
from datetime import datetime

class GoldenTechStore(BaseScraper):

    def __init__(self, headers, base_url):
        super().__init__(headers, base_url)

    def fetch(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")
            
            # El link ya tiene el filtro asique solo bajamos con scroll infinito de a poco
            while True:
                # Scrolleamos paso a paso en vez de ir directo al fondo para que las publicaciones vayan apareciendo
                page.evaluate("window.scrollBy(0, 1000)")
                page.wait_for_timeout(1000)
                
                # Chequeamos el progreso
                current_scroll = page.evaluate("window.scrollY + window.innerHeight")
                total_height = page.evaluate("document.body.scrollHeight")
                
                # Si llegamos cerca del fondo (con margen de error de 50px)
                if current_scroll >= total_height - 50:
                    # Esperamos la respuesta de la web para cargar los nuevos productos
                    page.wait_for_timeout(2500)
                    new_total_height = page.evaluate("document.body.scrollHeight")
                    
                    if new_total_height == total_height:
                        break # Ya cargó todo el infinito, podemos salir
                
            soup = BeautifulSoup(page.content(), 'html.parser')
        return soup

    def parse(self, html):
        return html.find_all('article', class_='product')

    def extract_products(self, parsed):
        products = []
        for product in parsed:
            try:
                ################### NOMBRE ###################
                name_tag = product.find('h2', class_='post_title')
                if not name_tag:
                    continue
                
                name = name_tag.text.strip().replace('\n', '')
                
                # Checkeo extra por si el filtro falla
                name_lower = name.lower()
                if 'placa de video' not in name_lower and 'rtx' not in name_lower and 'rx' not in name_lower and 'gtx' not in name_lower and 'vga' not in name_lower:
                    continue

                ################### IMAGEN ###################
                img_url = ""
                img_container = product.find('div', class_='post_image')
                if img_container:
                    img_tag = img_container.find('img')
                    if img_tag:
                        img_url = img_tag.get('src') or img_tag.get('data-src') or ""
                
                ################### URL ###################
                url_tag = name_tag.find('a')
                if not url_tag:
                    continue
                url = url_tag.get('href')
                final_url = url if url.startswith('http') else f"{self.base_url.rstrip('/')}{url}"
                
                ################### PRECIO ###################
                price = 0
                price_span = None
                all_divs = product.find_all('div', class_='w-html')
                for div in all_divs:
                    if 'Precio Efectivo' in div.text:
                        bdi = div.find('bdi')
                        if bdi:
                            price_text = bdi.text.split(',')[0]
                            price = int(clean_price(price_text))
                            price_span = bdi
                            break
                
                if not price_span:
                    price_tag = product.find('p', class_='price')
                    if price_tag:
                        bdi = price_tag.find('bdi')
                        if bdi:
                            price_text = bdi.text.split(',')[0]
                            price = int(clean_price(price_text))
                
                if price == 0:
                    continue
                
                ################### CHIPSET ###################
                chipset = find_chipset(name)
                
                ################### FECHA ###################
                date = datetime.now()
                
                ################### OUTLET ###################
                is_outlet = False
                if 'outlet' in product.get('class', []) or 'outlet' in name.lower() or 'usada' in name.lower():
                    is_outlet = True

                ################### GPU ###################
                gpu = Gpu(name, chipset, price, final_url, img_url, is_outlet, 'Golden Tech Store', date)
                
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


