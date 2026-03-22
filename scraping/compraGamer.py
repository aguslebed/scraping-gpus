from baseScrapingClass import BaseScraper
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from Gpu import Gpu


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
            soup = BeautifulSoup(page.content(), 'html.parser')
        return soup

    def parse(self, html):
        return html.findAll('a', class_='product-card cg__primary-card medium vertical responsive notSelected')

    def extract_products(self, parsed):
        products = []
        for product in parsed:
            try:
                if not product.find('img').has_attr('src'):
                    continue
                else:
                    img_url = product.find('img')['src']
                name = product.find('h3', class_='product-card__title cg__fw-400 mb-2 ng-star-inserted').text
                price = product.find('span', class_='txt_price').text
                url = product.get('href')
                final_url = f"{self.base_url}{url}"
                gpu = Gpu(name,chipset, price, final_url, img_url, False, 'Compra Gamer')
                products.append(gpu.get_obj())    
                splited_name = name.split()
                print(splited_name)
            except Exception as e:
                print(f"Error al extraer el producto: {e}") 
        
        return products
            

    def scrape(self):
        html = self.fetch(self.base_url)
        parsed = self.parse(html)
        return self.extract_products(parsed)