from playwright.sync_api import sync_playwright

url = "https://www.maximus.com.ar/"
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, wait_until="domcontentloaded")
    page.get_by_placeholder("Buscar en Maximus").fill("placa de video")
    page.get_by_placeholder("Buscar en Maximus").press("Enter")
    page.wait_for_timeout(5000)
    with open("maximus_test.html", "w") as f:
        f.write(page.content())
    print("Done")
