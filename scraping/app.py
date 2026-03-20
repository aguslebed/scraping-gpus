import compraGamer

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3' 
}
base_url = 'https://compragamer.com/productos?criterio=placa%20de%20video'

compragamer = compraGamer.CompraGamer(headers, base_url)
html_compraGamer = compragamer.fetch()
parsedHtml_compraGamer = compragamer.parse(html_compraGamer)
print(len(parsedHtml_compraGamer))