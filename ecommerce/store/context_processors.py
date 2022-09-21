# here we are working with cart and cart models.
#  category
from .models import Category
#  cart
from .models import Cart, CartItem
from .views import _cart_id


def menu_links(request):
    links = Category.objects.all()  # first we fetch all the categories form the category app as a 'list'.
    return dict(links=links)  # here we are returning the links as a dictionary


def counter(request):
    cart_count = 0  # initialize the cart_count to zero else it will throw an error.
    if 'admin' in request.path:
        return {}  # for admin we pass empty dictionary, because we don't need to see that.
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))  # this cart id will have the session key
            cart_items = CartItem.objects.all().filter(
                cart=cart[:1])  # here we needed only one item from each product in the cart

            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:  # if the cart doesn't exist'
            cart_count = 0

    return dict(cart_count=cart_count)