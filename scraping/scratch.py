import sys, os
from playwright.sync_api import sync_playwright

url = "https://www.maximus.com.ar/"
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(extra_http_headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
    
    page.goto(url, wait_until="domcontentloaded")
    page.get_by_placeholder("Buscar en Maximus").fill("placa de video")
    page.get_by_placeholder("Buscar en Maximus").press("Enter")
    page.wait_for_timeout(5000)
    with open("maximus_test.html", "w", encoding="utf-8") as f:
        f.write(page.content())
    print("Done")
