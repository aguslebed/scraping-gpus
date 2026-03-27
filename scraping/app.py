import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tiendas'))

from tiendas import goldenTechStore, compraGamer, maximusGaming
from utils import split_price
from db import insert_price, insert_gpu

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3' 
    }
    
    # 1. Agrega aquí las instancias de tus nuevos scrapers
    scrapers = [
        compraGamer.CompraGamer(headers, 'https://compragamer.com'),
        maximusGaming.Maximus(headers, 'https://www.maximus.com.ar'),
        goldenTechStore.GoldenTechStore(headers, 'https://goldentechstore.com.ar/placas-de-video/'),
        
    ]
    
    # 2. Iteramos sobre cada tienda en la lista
    for scraper in scrapers:
        tienda_nombre = scraper.__class__.__name__
        print(f"\n--- Iniciando extracción en {tienda_nombre} ---")
        
        try:
            resultados = scraper.scrape()
            print(f"[{tienda_nombre}] Se extrajeron {len(resultados)} productos exitosamente.")
            
            # 3. Guardamos los resultados
            for gpu in resultados:
                price, gpu_data = split_price(gpu)
                
                # Insert or find the GPU and get its MongoDB ObjectId
                gpu_id = insert_gpu(gpu_data)
                
                # Link the price to the GPU
                if gpu_id:
                    price['gpu_id'] = gpu_id
                    insert_price(price)
            
            print(f"[{tienda_nombre}] Precios guardados exitosamente.\n")
                    
        except Exception as e:
            print(f"Error crítico scrapeando la tienda {tienda_nombre}: {e}")

if __name__ == "__main__":
    main()
