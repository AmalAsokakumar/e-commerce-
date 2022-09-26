from django.urls import path
from .views import place_order, orders, payments

urlpatterns = [
    #  orders
    path('place-order/', place_order, name='place_order'),
    path('payments/', payments, name='payments'),
    path('', orders, name='orders'),
]