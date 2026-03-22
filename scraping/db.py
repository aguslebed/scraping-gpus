from pymongo import MongoClient

try:
    client = MongoClient('localhost', 27017)
    database = client['Scraping']
    gpu_collection = database['gpus']
    price_colection = database['prices']

except Exception as e:
    print(f'Error al conectar a la base de datos: {e}')