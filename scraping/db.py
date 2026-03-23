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
        # Buscamos si la GPU ya existe por su URL (que es única)
        existing_gpu = gpu_collection.find_one({'url': gpu['url']})
        if existing_gpu:
            return existing_gpu['_id']
        else:
            result = gpu_collection.insert_one(gpu)
            return result.inserted_id
    except Exception as e:
        print(f'Error al insertar la gpu: {e}')
        return None

def insert_price(price):
    try:
        price_colection.insert_one(price)
    except Exception as e:
        print(f'Error al insertar el precio: {e}')