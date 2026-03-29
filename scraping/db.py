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
        gpu['in_stock'] = True
        
        # Buscamos si la GPU ya existe por su URL (que es única)
        existing_gpu = gpu_collection.find_one({'url': gpu['url']})
        if existing_gpu:
            # Si existe, actualizamos su última fecha y la volvemos a poner en stock
            update_doc = {
                '$set': {
                    'last_update': gpu['last_update'],
                    'in_stock': True
                }
            }
            gpu_collection.update_one({'_id': existing_gpu['_id']}, update_doc)
            return existing_gpu['_id']
        else:
            result = gpu_collection.insert_one(gpu)
            return result.inserted_id
    except Exception as e:
        print(f'Error al insertar o actualizar la gpu: {e}')
        return None

def mark_out_of_stock(store_name, start_time):
    try:
        result = gpu_collection.update_many(
            {'store': store_name, 'last_update': {'$lt': start_time}},
            {'$set': {'in_stock': False}}
        )
        return result.modified_count
    except Exception as e:
        print(f'Error al marcar sin stock para {store_name}: {e}')
        return 0

def insert_price(price):
    try:
        # Prevenir inserción de precios erróneos (0 o negativos)
        if price is None or price.get('price', 0) <= 0:
            return

        # Obtenemos el inicio y fin del día actual según la fecha del precio
        day_start = price['date'].replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = price['date'].replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # Filtramos por esa misma placa de video y en el día de hoy
        filter_query = {
            'gpu_id': price['gpu_id'],
            'date': {'$gte': day_start, '$lte': day_end}
        }
        
        # Buscamos si ya hay un precio guardado hoy
        existing_price = price_colection.find_one(filter_query)
        
        if existing_price:
            # Si el precio es exactamente igual al que ya estaba hoy, no hacemos nada.
            if existing_price['price'] == price['price']:
                return
            else:
                # Si el precio cambió durante el mismo día, actualizamos el registro
                # con el nuevo precio y la nueva hora exacta
                update_doc = {
                    '$set': {
                        'price': price['price'],
                        'date': price['date'],
                        'store': price['store']
                    }
                }
                price_colection.update_one({'_id': existing_price['_id']}, update_doc)
        else:
            # Si no hay ningún precio hoy para esta GPU, lo insertamos nuevo
            price_colection.insert_one(price)
            
    except Exception as e:
        print(f'Error al insertar el precio: {e}')