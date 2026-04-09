from bs4 import BeautifulSoup

with open("maximus_test.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

products = soup.find_all('div', class_=lambda x: x and 'mxCardProduct' in x)
if products:
    p = products[0]
    print(p.prettify()[:1000])

