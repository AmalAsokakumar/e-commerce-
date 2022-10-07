from django.urls import path
from .views import (
    place_order,
    orders,
    payments,
    order_complete,
    cod_payment,
    order_payment,
    callback,
)

urlpatterns = [
    #  orders
    path("place-order/", place_order, name="place_order"),
    path("cod/", cod_payment, name="cod_payment"),
    path("payments/", payments, name="payments"),
    path("order-complete/", order_complete, name="order_complete"),
    path("", orders, name="orders"),
    path("razor-payment/", order_payment, name="razor_payment"),
    path("callback/", callback, name="callback"),
]
