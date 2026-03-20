from baseScrapingClass import BaseScraper
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


class CompraGamer(BaseScraper):

    def __init__(self, headers, base_url):
        super().__init__(headers, base_url)

    def fetch(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(self.base_url, wait_until="networkidle")
            soup = BeautifulSoup(page.content(), 'html.parser')
        return soup

    def parse(self, html):
        return html.findAll('a', class_='product-card cg__primary-card medium vertical responsive notSelected')

    def extract_products(self, parsed):
        pass

    def scrape(self, url):
        html = self.fetch(url)
        parsed = self.parse(html)
        return self.extract_products(parsed)