from django.urls import path
from . import views

urlpatterns = [
    path('gpus', views.get_gpus, name='get_gpus'),
    path('prices', views.get_prices, name='get_prices'),
]
