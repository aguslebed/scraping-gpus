import compraGamer
from utils import split_price
from db import insert_price, insert_gpu

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3' 
}
base_url_compraGamer = 'https://compragamer.com'

compragamer = compraGamer.CompraGamer(headers, base_url_compraGamer)

for gpu in compragamer.scrape():
    price, gpu = split_price(gpu)
    print(price)
    print(gpu)
    obj = insert_price(price)
    #db.insert_gpu(gpu)
