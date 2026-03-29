import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'tiendas'))
from bs4 import BeautifulSoup

# We need the class logic to test it
from tiendas.compraGamer import CompraGamer

def test():
    cg = CompraGamer({}, 'https://compragamer.com')
    with open('mock html/CompraGamer_files/ProductoCompraGamer.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    parsed = cg.parse(soup)
    print(f"Parsed items: {len(parsed)}")
    
    products = cg.extract_products(parsed)
    print(f"Extracted items: {len(products)}")

if __name__ == "__main__":
    test()
