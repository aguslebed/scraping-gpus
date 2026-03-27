from abc import ABC, abstractmethod

class BaseScraper(ABC):

    def __init__(self, headers, base_url):
        self.headers = headers
        self.base_url = base_url


    @abstractmethod
    def fetch(self, url):
        pass

    @abstractmethod
    def parse(self, html):
        pass

    @abstractmethod
    def extract_products(self, parsed):
        pass

    def scrape(self, url):
        html = self.fetch(url)
        parsed = self.parse(html)
        return self.extract_products(parsed)