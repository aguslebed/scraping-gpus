import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tiendas'))

from tiendas.fullHard import FullH4rd

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    scraper = FullH4rd(headers, 'https://www.fullh4rd.com.ar')
    
    print("\n--- Iniciando extracción en FullH4rd (Test Live) ---")
    resultados = scraper.scrape()
    print(f"[{scraper.__class__.__name__}] Se extrajeron {len(resultados)} productos exitosamente.")
    
    for rp in resultados[:3]:
        print(rp)

if __name__ == "__main__":
    main()
