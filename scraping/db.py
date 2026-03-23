from pymongo import MongoClient

try:
    client = MongoClient('localhost', 27017)
    database = client['Scraping']
    gpu_collection = database['gpus']
    price_colection = database['prices']

except Exception as e:
    print(f'Error al conectar a la base de datos: {e}')


def insert_gpu(gpu):
    try:
        gpu_collection.insert_one(gpu)
    except Exception as e:
        print(f'Error al insertar la gpu: {e}')


def insert_price(price):
    try:
        price_colection.insert_one(price)
    except Exception as e:
        print(f'Error al insertar el precio: {e}')