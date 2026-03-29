from bs4 import BeautifulSoup
import json
import sys

with open('/home/agustin/Escritorio/scraping gpus/scraping/mock html/FullHardBody.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
# Find all divs that contain a price
price_divs = soup.find_all('div', class_='price')
print(f"Found {len(price_divs)} price divs")

if price_divs:
    # Get the parent item for the first one
    parent_item = price_divs[0].find_parent('div', class_='item')
    print("--- First item HTML: ---")
    print(parent_item.prettify()[:1500])
