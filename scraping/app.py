import compraGamer

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3' 
}
base_url_compraGamer = 'https://compragamer.com/productos?criterio=placa%20de%20video'

compragamer = compraGamer.CompraGamer(headers, base_url_compraGamer)

print(compragamer.scrape())