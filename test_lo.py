import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scraping'))

from tiendas.libreOpcion import LibreOpcion

def test():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3' 
    }
    lo = LibreOpcion(headers, 'https://www.libreopcion.com/placas-de-video')
    
    print("Testing LO scraper...")
    res = lo.scrape()
    print(f"Ended testing. Results: {len(res)}")
    for r in res[:5]:
        print(r)

if __name__ == '__main__':
    test()
