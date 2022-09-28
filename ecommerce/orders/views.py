from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from store.models import CartItem
from store.models import Product
from .models import Order, OrderProduct
from .forms import OrderForm
from .models import Payment
import datetime
import json


def payments(request):
    body = json.loads(request.body)
    print(
        body
    )  # {'orderID': '0022092621', 'transID': '6JT072363T708401U', 'payment_method': 'PayPal', 'status':
    # 'COMPLETED'}
    # now store these details inside the payment model`
    order = Order.objects.get(
        user=request.user, is_ordered=False, order_number=body["orderID"]
    )
    payment = Payment(
        user=request.user,
        payment_id=body["transID"],
        payment_method=body["payment_method"],
        amount_paid=order.order_total,
        status=body["status"],
    )
    print(payment)
    payment.save()
    order.payment = payment  # we need to update the order model also.
    order.is_ordered = True
    order.save()  # now the order is successful
    # move the cart items to order Product table,
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        order_product = (
            OrderProduct()
        )  # we have created an object of this model and assign these values to it.
        order_product.order_id = (
            order.id
        )  # order is a foreign object of OrderProduct model.
        order_product.payment = (
            payment  # which is the object that we just created above
        )
        order_product.user_id = request.user.id
        order_product.product_id = (
            item.product_id
        )  # this field must be created by the database.
        order_product.quantity = item.quantity
        order_product.product_price = (
            item.product.price
        )  # product is a foreign key of CartItem model
        order_product.ordered = True  # by this time product must have been ordered
        order_product.save()
        # making the changes to product variations
        # we cannot directly assign values to many to many fields
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        order_product = OrderProduct.objects.get(
            id=order_product.id
        )  # the above save have alredy generatedt id for OrderProduct
        order_product.variations.set(product_variation)
        order_product.save()
        # reduce the quantity of the stock
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
    # clear the cart
    CartItem.objects.filter(user=request.user).delete()
    # sent order received message to customer
    # this part is for later
    # sent order number and  translation id -> sentData() via JsonResponse
    data = {
        "order_number": order.order_number,
        "transID": payment.payment_id,
    }
    return JsonResponse(
        data
    )  # this data wil go to the place where it came from { in html sentData()


def orders(request):
    return render(request, "order_complete.html")


# Create your views here
# first need to check if the user have an item in caret, if not redirect them back to store page.
def place_order(request, total=0, quantity=0):
    print("we are inside the place order section \n\n\n")
    instance_user = request.user
    #  if the cart count  is less-than or equal to zero, he doesn't have any cart item.
    cart_items = CartItem.objects.filter(user=instance_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect("store")
    # actual code 1, store the post request inside the order model and generate the order number.
    grand_total = 0
    discount = 0
    tax = 0
    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax
    if request.method == "POST":
        print("request.post", request.POST)
        print("a post method received \n\n\n")
        form = OrderForm(request.POST)
        print(form)
        print("now form is validating \n\n")
        if form.is_valid():
            print("the form is valid \n\n")
            # store the date to -> Order model
            data = Order()  # creating an instance of the model
            data.user = instance_user
            data.first_name = form.cleaned_data["first_name"]
            data.last_name = form.cleaned_data["last_name"]
            data.email = form.cleaned_data["email"]
            data.phone = form.cleaned_data["phone"]
            data.address_line_1 = form.cleaned_data["address_line_1"]
            data.address_line2 = form.cleaned_data["address_line_2"]
            data.landmark = form.cleaned_data["landmark"]
            data.city = form.cleaned_data["city"]
            data.pincode = form.cleaned_data["pincode"]
            data.country = form.cleaned_data["country"]
            data.state = form.cleaned_data["state"]
            data.order_note = form.cleaned_data["order_note"]
            # calculated datas
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get("REMOTE_ADDR")  # this will give you the user ip.
            data.save()  # it will create a primary key which can be used to create order id
            print("basic details saved \n\n\n")
            # generate order number
            yr = int(datetime.date.today().strftime("%y"))  # year
            dt = int(datetime.date.today().strftime("%d"))  # date
            mt = int(datetime.date.today().strftime("%m"))  # month
            d = datetime.date(yr, mt, dt)  # stored here
            current_date = d.strftime(
                "%Y%m%d"
            )  # -> 20220923  now concatenate it with order number
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(
                user=instance_user, is_ordered=False, order_number=order_number
            )
            context = {
                "order": order,
                "cart_items": cart_items,
                "total": total,
                "grand_total": grand_total,
            }
            return render(request, "payments.html", context)
        else:
            print("form is failed to validate \n\n\n")
            return redirect("checkout")

    return HttpResponse("place order page under development")


def order_complete(request):
    order_number = request.GET.get("order_number")
    transID = request.GET.get("payment_id")
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        sub_total = 0
        for i in ordered_products:
            sub_total += i.product_price * i.quantity
        payment = Payment.objects.get(payment_id=transID)
        context = {
            "order": order,
            "ordered_products": ordered_products,
            "order_number": order.order_number,
            "transID": payment.payment_id,
            "payment": payment,
            "sub_total": sub_total,
        }
        return render(request, "order_complete.html", context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        print(
            "\n\n entered inside the except block and skipped the payment rendering page"
        )
        return redirect("user_home")
