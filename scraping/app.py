import compraGamer
from utils import split_price
from db import insert_price, insert_gpu

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3' 
}
base_url_compraGamer = 'https://compragamer.com'

compragamer = compraGamer.CompraGamer(headers, base_url_compraGamer)

for gpu in compragamer.scrape():
    price, gpu_data = split_price(gpu)
    
    # Insert or find the GPU and get its MongoDB ObjectId
    gpu_id = insert_gpu(gpu_data)
    
    # Link the price to the GPU
    if gpu_id:
        price['gpu_id'] = gpu_id
        insert_price(price)
        print(f"Price for {gpu_data['name']} inserted correctly.")
