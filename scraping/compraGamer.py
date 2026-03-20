from baseScrapingClass import BaseScraper
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


class CompraGamer(BaseScraper):

    def __init__(self, headers, base_url):
        super().__init__(headers, base_url)

    def fetch(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")
            soup = BeautifulSoup(page.content(), 'html.parser')
        return soup

    def parse(self, html):
        return html.findAll('a', class_='product-card cg__primary-card medium vertical responsive notSelected')

    def extract_products(self, parsed):
        products = []
        for product in parsed:
            img_url = product.find('img')
            name = product.find('h3', class_='product-card__title cg__fw-400 mb-2 ng-star-inserted').text
            price = product.find('span', class_='txt_price').text
            url = product.get('href')
            products.append({'name': name, 'price': price, 'url': url, 'img_url': img_url})
        
        return products
            

    def scrape(self):
        html = self.fetch(self.base_url)
        parsed = self.parse(html)
        return self.extract_products(parsed)