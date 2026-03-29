import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tiendas'))

from tiendas import goldenTechStore, compraGamer, maximusGaming, fullHard, mexx, libreOpcion, venex, quantumHardStore
from utils import split_price
from db import insert_price, insert_gpu, mark_out_of_stock
from datetime import datetime

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3' 
    }
    
    scrapers = [
        compraGamer.CompraGamer(headers, 'https://compragamer.com'),
        maximusGaming.Maximus(headers, 'https://www.maximus.com.ar'),
        goldenTechStore.GoldenTechStore(headers, 'https://goldentechstore.com.ar/placas-de-video/'),
        fullHard.FullH4rd(headers, 'https://www.fullh4rd.com.ar'),
        mexx.Mexx(headers, 'https://www.mexx.com.ar/productos-rubro/placas-de-video/'),
        libreOpcion.LibreOpcion(headers, 'https://www.libreopcion.com/placas-de-video'),
        venex.Venex(headers, 'https://www.venex.com.ar/componentes-de-pc/placas-de-video'),
        quantumHardStore.QuantumHardStore(headers, 'https://quantumhardstore.com/componentes/placas-de-video/')
    ]

    for scraper in scrapers:
        tienda_nombre = scraper.__class__.__name__
        print(f"\n--- Iniciando extracción en {tienda_nombre} ---")
        start_time = datetime.now()
        
        try:
            resultados = scraper.scrape()
            print(f"[{tienda_nombre}] Se extrajeron {len(resultados)} productos exitosamente.")
            
            for gpu in resultados:
                price, gpu_data = split_price(gpu)
                
                gpu_id = insert_gpu(gpu_data)
                
                if gpu_id:
                    price['gpu_id'] = gpu_id
                    insert_price(price)
            
            marked = mark_out_of_stock(tienda_nombre, start_time)
            print(f"[{tienda_nombre}] Precios guardados exitosamente. {marked} tarjetas marcadas sin stock.\n")
                    
        except Exception as e:
            print(f"Error crítico scrapeando la tienda {tienda_nombre}: {e}")

if __name__ == "__main__":
    main()
