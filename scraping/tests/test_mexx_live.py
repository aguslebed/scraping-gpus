import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'tiendas'))

from tiendas.mexx import Mexx

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    scraper = Mexx(headers, 'https://www.mexx.com.ar/productos-rubro/placas-de-video/')
    
    print("\n--- Iniciando extracción en Mexx (Test Live) ---")
    resultados = scraper.scrape()
    print(f"[{scraper.__class__.__name__}] Se extrajeron {len(resultados)} productos exitosamente.")
    
    for rp in resultados[:5]:
        print(f"  [{rp['store']}] {rp['name']} — ${rp['price']} — chipset: {rp['chipset']}")

if __name__ == "__main__":
    main()
