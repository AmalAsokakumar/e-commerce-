from django.urls import path
from .views import (
    place_order,
    orders,
    payments,
    order_complete,
    cod_payment,
    razorpay_payment,
    payment_handler,
    # order_payment,
    # callback,
    # success,
    # order,
)

urlpatterns = [
    #  orders
    path("place-order/", place_order, name="place_order"),
    path("cod/", cod_payment, name="cod_payment"),
    path("payments/", payments, name="payments"),
    path("order-complete/", order_complete, name="order_complete"),
    path("", orders, name="orders"),
    path("razorpay/", razorpay_payment, name="razorpay"),
    path("razorpay-payment/", payment_handler, name="payment_handler"),
    # path("order/", order, name="order"),
    # path("success/", success, name="success"),
    # path("payment/", order_payment, name="payment"),
    # path("callback/", callback, name="callback"),
]
