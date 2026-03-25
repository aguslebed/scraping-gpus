from django.http import JsonResponse
from pymongo import MongoClient

# Create your views here.
client = MongoClient('localhost', 27017)
db = client['Scraping']

def get_gpus(request):
    try:
        gpus = list(db['gpus'].find())
        for gpu in gpus:
            gpu['_id'] = str(gpu['_id'])
        return JsonResponse(gpus, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_prices(request):
    try:
        prices = list(db['prices'].find())
        for price in prices:
            price['_id'] = str(price['_id'])
            if 'gpu_id' in price:
                price['gpu_id'] = str(price['gpu_id'])
            if 'date' in price:
                price['date'] = price['date'].isoformat()
        return JsonResponse(prices, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

