from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse

# category imports
from .forms import CategoryForm
from .models import Category

# brand imports
from .forms import BrandForm
from .models import Brand

# products
from .models import Product
from .forms import ProductForm

# cart views
# for private function in product details
from .models import CartItem
from .models import Cart
from .models import Variation
from django.core.exceptions import ObjectDoesNotExist

# for paginator function
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# for search function
from django.db.models import Q

# for login in required activities
from django.contrib.auth.decorators import login_required

# for dynamic routing, request library is imported
import requests

# for coupon

from .models import Coupon, UsedCoupon
from .forms import CouponForm, UsedCouponForm

# offers
from store.models import CategoryOffer
from store.models import BrandOffer
from store.models import ProductOffer


# basic views
def home(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect("admin_home")
    return render(request, "user/index.html", {})


def contact(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect("admin_home")
    return render(request, "user/contact.html", {})


def about(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect("admin_home")
    return render(request, "user/about.html", {})


# categories views
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(
                "category_success"
            )  # if this is valid it will invoke the upload_pic function.
    else:
        form = CategoryForm()
    return render(request, "category.html", {"form": form})


def upload_pic(request):
    messages.success(request, "Category added successfully ")
    return redirect("add_category")
    # return HttpResponse('category added successful')


def view_category(request):
    form = Category.objects.all()
    context = {"form": form, "title": "Category View"}
    return render(request, "view_category.html", context)


def delete_category(request, id):
    print("\n\n delete category \n\n")
    user = request.user
    if user.is_authenticated:
        Category.objects.filter(pk=id).delete()
        return redirect("category_view")
    else:
        return redirect("category_view")


def edit_category(request, id):
    print("\n\nEdit category")
    user = request.user
    if user.is_authenticated:
        print("super user authentication completed\n\n")
        category = get_object_or_404(Category, pk=id)
        form = CategoryForm(
            request.POST or None, request.FILES or None, instance=category
        )
        if form.is_valid():
            edit = form.save(commit=False)
            edit.save()
            return redirect("category_view")
        return render(request, "edit_category.html", {"form": form})
    return redirect("/")


# brand views
def add_brand(request):
    if request.method == "POST":
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("brand_success")
    else:
        form = BrandForm()
        return render(request, "brand.html", {"form": form})


def upload_pic_(request):
    messages.success(request, "Brand added successfully ")
    return redirect("add_brand")


def view_brand(request):
    print("\n \ninside brand view fn  \n\n")
    form = Brand.objects.all()
    context = {"form": form, "title": "Brand View"}
    return render(request, "view_brand.html", context)


def delete_brand(request, id):
    print("\n \n deleting brand \n\n")
    user = request.user
    if user.is_authenticated:
        Brand.objects.filter(pk=id).delete()
        return redirect("brand_view")
    else:
        return redirect("brand_view")  # should be replaced to login in view


def edit_brand(request, id):
    print("\n\n edit_ brand \n")
    user = request.user
    if user.is_superuser:
        print("super user authentication completed  \n\n")
        brand = get_object_or_404(Brand, pk=id)  # to prepopulated the form
        # brand = Brand.objects.get(pk=id) # getting details of the object from models using primary key
        form = BrandForm(request.POST or None, request.FILES or None, instance=brand)
        if form.is_valid():
            print("form is valid ")
            # form.save() # saving the changes.
            edit = form.save(
                commit=False
            )  # in order to add this condition i disable the above condition.
            edit.save()  #
            return redirect("brand_view")
        return render(request, "edit_brand.html", {"form": form, "type": "Brand "})
    return redirect(
        "/"
    )  # un authentication users will be redirected to default page {{ need to change this field }}
    # return render(request,'edit_brand.html')


# product views
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(
                "product_success"
            )  # if this is valid it will invoke the upload_pic function.
    else:
        form = ProductForm()
    return render(request, "product.html", {"form": form})


def upload_pic_pro(request):
    messages.success(request, "Product added successfully ")
    return redirect("add_product")


def view_product(request):
    form = Product.objects.all()
    context = {"form": form, "title": "Product View"}
    return render(request, "view_Product.html", context)


def delete_product(request, id):
    print("\n\n delete product \n\n")
    user = request.user
    if user.is_authenticated:
        Product.objects.filter(pk=id).delete()
        return redirect("product_view")
    else:
        return redirect("/")


def edit_product(request, id):
    print("\n\nEdit product")
    user = request.user
    if user.is_authenticated:
        print("super user authentication completed\n\n")
        product = get_object_or_404(Product, pk=id)
        form = ProductForm(
            request.POST or None, request.FILES or None, instance=product
        )
        if form.is_valid():
            edit = form.save(commit=False)
            edit.save()
            return redirect("product_view")
        return render(request, "editCB.html", {"form": form})
    return redirect("/")


# store views
def store(
    request, category_slug=None
):  # we are passing a slug field to filter the content based on the user request
    categories = None
    products = None
    if (
        category_slug is not None
    ):  # if the slug is not none, we have to do some database operations.
        categories = get_object_or_404(
            Category, slug=category_slug
        )  # what this query set will do is like it will
        # look for a requested objects if not found it will show us a 404 error. (,in Category models slug field )
        products = Product.objects.filter(
            category=categories, is_available=True
        )  # to get all the product in the
        # categories if it's available.these three lines of codes are repeated.
        paginator = Paginator(
            products, 6
        )  # product is the model object that we wanted to print, (model_object,
        # number_of_product) is the number of product that we wanted to show.
        page = request.GET.get(
            "page"
        )  # we will capture the url that comes with the page number ('page') < which we
        # enter to navigate like slug
        paged_products = paginator.get_page(page)
        product_count = (
            products.count()
        )  # to count the products in the category that we have chosen.
    else:  # if slug field is empty that is we haven't chosen a category
        products = Product.objects.all().filter(is_available=True).order_by("id")
        paginator = Paginator(
            products, 6
        )  # product is the model object that we wanted to print, (model_object,
        # number_of_product) is the number of product that we wanted to show.
        page = request.GET.get(
            "page"
        )  # we will capture the url that comes with the page number ('page') < which we
        # enter to navigate like slug
        paged_products = paginator.get_page(
            page
        )  # now we have 6 products stored in this page because of
        # "paginator = Paginator(products,6) " function.
        product_count = (
            products.count()
        )  # we are finding product count using python function.
    context = {
        "products": paged_products,  #
        # 'products': products,
        # we use paginator to customize the number of product that we wanted to show
        "product_count": product_count,
    }
    return render(request, "user/shop.html", context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug
        )  # here we wanted to
        # get a hold of the slug of the category which is present in the category app. (__slug is a method to access
        # the slug field of that category = which should be matched against the slug field in the url request)
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request), product=single_product
        ).exists()  # __cart
        # to check the cart model ('cart'  < __cart_id ), because cart is a foreign key of cart item. so first we are
        # accessing the cart first then through it we are accessing ' cart_id' < so that is the reason we are using
        # the under score. '_cart_id(request) is the private function we created inside the cart view function. then
        # it is filter by single product.
        # return HttpResponse(in_cart)   # if the above query returns anything, it will be true  then we are not
        # gonna show an add button. exit() # if the above condition is true it will simply exit the code.
    except Exception as e:
        raise e
    context = {
        "single_product": single_product,  # creating a context dictionary.
        "in_cart": in_cart,  # check result of the  item is already in cart or not.
    }
    return render(request, "user/shop_single.html", context)


def search(request):
    products = None
    if "keyword" in request.GET:
        keyword = request.GET["keyword"]
        if keyword:
            products = Product.objects.order_by("-created_date").filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
            )  # "filter(description__icontains=keyword ,
            # product_name__icontains=keyword , brand_name__icontains=keyword) "in the filter section we can use & and
            # , for and operations and 'Q' - or query set for or operations
            # products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(
            # product_name__icontains=keyword))
            product_count = products.count()
    context = {
        "products": products,
        "product_count": product_count,
    }
    return render(request, "user/shop.html", context)


# cart                                                              # this is a private function to create cart id
# using a section id
def _cart_id(request):  # this is a private function because we use an _ denote that
    cart = request.session.session_key
    if (
        not cart
    ):  # check if the cart variable is empty if it is we are gonna create a one.
        cart = request.session.create()
        # print(' \n\n new session key is created ')
    return cart


def cart(request, total=0, quantity=0, offer_price_=0, cart_items=None):
    # print('we are currently inside the cart page')
    # return HttpResponse('we are in future cart page')
    a = []
    price = 0
    total_price = 0
    tax = 0
    grand_total = 0
    discount = 0
    if "coupon_code" in request.session:
        print(request.session["coupon_code"])
        coupon = Coupon.objects.get(coupon_code=request.session["coupon_code"])
        discount = coupon.amount
    try:
        # this conditions is for customers who just logged in, and  they can carry along there guest cart along with it.
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            # this will work for the guest users,
            cart = Cart.objects.get(
                cart_id=_cart_id(request)
            )  # calling the above private function for the cart id.
            # because the user is not logged in hence, he needs a cart id to keep cart items, which is created above.
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        quantity = 0
        for cart_item in cart_items:
            # we are processing each and every item inside the car_item list.
            total += cart_item.product.price * cart_item.quantity
            print("total", total)
            offer_price_ += cart_item.product.product_offer * cart_item.quantity

            a.append(offer_price_)
            print(
                " cart_item.quantity",
                cart_item.quantity,
                "cart item_ offer price :",
                offer_price_,
                "cart_item.product.product_offer",
                cart_item.product.product_offer,
            )
            print("cart item quantity", cart_item.quantity)
            print("offer price", offer_price_)
            # offer setting

            # after these calculations we can add the offers .
            quantity = cart_item.quantity
            price = round(total, 2)
            tax = round((18 * total) / 100, 2)
            total_price = round(total + tax, 2)
            offer_price = round(total_price - offer_price_, 2)
            grand_total = round(offer_price - discount, 2)

    except ObjectDoesNotExist:
        pass  # we can simply pass it.

    for i in range(0, len(a)):
        print("array list \n the offer items are :", a[i])
    context = {
        "price": price,
        "discount": discount,
        "offer_price": offer_price_,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "total_price": total_price,
        "grand_total": grand_total,
    }
    return render(request, "cart/cart_final.html", context)


def add_cart(request, product_id):
    #  we are creating current user variable for a user instance
    p_offer = 0
    c_offer = 0
    b_offer = 0
    user_instance = request.user
    product = Product.objects.get(id=product_id)
    # here i am  going to set up offers
    if BrandOffer.objects.filter(brand=product.brand).order_by("-brand_offer").first():
        brand = (
            BrandOffer.objects.filter(brand=product.brand)
            .order_by("-brand_offer")
            .first()
        )
        b_offer = brand.brand_offer
        if "b_offer" is not None:
            print("brand offer object :", brand, ",offer value ", b_offer)
    if ProductOffer.objects.filter(product=product).order_by("-product_offer").first():
        product_ = (
            ProductOffer.objects.filter(product=product)
            .order_by("-product_offer")
            .first()
        )
        if "p_offer" is not None:
            p_offer = product_.product_offer
            print(
                "product offer object : ",
                product_,
                "product offer value : ",
                p_offer,
            )
    if (
        CategoryOffer.objects.filter(category=product.category)
        .order_by("-category_offer")
        .first()
    ):
        category_ = (
            CategoryOffer.objects.filter(category=product.category)
            .order_by("-category_offer")
            .first()
        )
        if "c_offer" is not None:
            c_offer = category_.category_offer
            print(
                "category offer object :",
                category_,
                "The category offer : ",
                c_offer,
            )
    offer_ = [p_offer, c_offer, b_offer]
    print("product offer ", p_offer)
    offer = max(offer_)
    print("highest offer is ", offer)
    #  saving the product offer value to product object.
    product.product_offer = offer
    # product_offer.product_offer = offer
    product.save()  # save product
    print("product offer is : ", product.product_offer)
    # check if the user is authenticated
    if user_instance.is_authenticated:
        product = Product.objects.get(id=product_id)  # get the product
        product_variation = []
        # here we are creation an empty list to hold all the variations. '.append' method is used to add values to it.
        if request.method == "POST":
            for (
                item
            ) in (
                request.POST
            ):  # this loop is created to accept whatever the variation that the admin is created
                # in there, it will a key value pair to accept it.
                key = item  # key will be stored her
                value = request.POST[key]  # value will be stored here
                try:
                    variation = Variation.objects.get(
                        product=product,
                        variation_category__iexact=key,
                        # made changes
                        variation_value__iexact=value,
                    )
                    product_variation.append(
                        variation
                    )  # in this step we are appending variations to the Variations list.
                except:
                    pass
            # in this entail section we are gonna change the cart with user
            # we are already authenticated hence we don't need a section to create a card id.
        is_cart_item_exists = CartItem.objects.filter(
            product=product, user=user_instance
        ).exists()
        #  here we have modified the filter query by changing the card_id to user.
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=user_instance)
            id = []
            ex_var_list = []  # created an empty list to store the variations
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            if product_variation in ex_var_list:
                # increase the item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:  # if cart doesn't have any items.
                item = CartItem.objects.create(
                    product=product, quantity=1, user=user_instance
                )
                if len(product_variation) > 0:
                    item.variations.clear()  #
                    item.variations.add(*product_variation)
                    # cart_item.quantity += 1                                        # it is commented because it is
                    # added above # to count the number of items in the cart.
                    item.save()  # save the cart item to the database
                    # print('\n new item added to the cart\n\n')
        else:
            # CartItem.DoesNotExist:                                       #if cart item is empty.
            cart_item = (
                CartItem.objects.create(  # things need to create a new cart are these
                    product=product,
                    quantity=1,
                    user=user_instance,
                )
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()  #
                cart_item.variations.add(*product_variation)
                cart_item.save()  # save the cart item to the database
                # print('\n\n items are added to the cart ')
                # return HttpResponse(cart_item.product)
                # exit()
        return redirect("view_cart")
    else:  # if the user is not authenticated.
        product = Product.objects.get(id=product_id)  # get the product
        product_variation = (
            []
        )  # here we are creation an empty list to hold all the variations. '.append' method is
        # used to add values to it.
        if request.method == "POST":
            for (
                item
            ) in (
                request.POST
            ):  # this loop is created to accept whatever the variation that the admin is created
                # in there, it will an key value pair to accept it.
                key = item  # key will be stored her
                value = request.POST[key]  # value will be stored here
                try:
                    variation = Variation.objects.get(
                        products=product,
                        variation_category__iexact=key,
                        variation_value__iexact=value,
                    )
                    # i means it is case insensitive  ( initial product is the field name of the variation model)
                    product_variation.append(
                        variation
                    )  # in this step we are appending variations to the Variations list.
                except:
                    pass
                    # print(' \n\n add cart',str(product_id))
                    # print (' \n\n inside the cart')
        try:
            # print(' \n looking for a cart')
            cart = Cart.objects.get(cart_id=_cart_id(request))
            # here we are adding the section id as cart id. to get that we use a private function.  Get
            # the cart, using the cart_id present in the session
        except Cart.DoesNotExist:  # if cart not exist, we are gonna create one.
            #                                                        print("\n\n cart does not exist")
            cart = Cart.objects.create(
                cart_id=_cart_id(
                    request
                )  # we will create a cart id using above private function.
            )
            cart.save()
            # print("\n\n new  cart created ") print("\n\n new cart is created") in a cart we can have a number ot item,
            # which can be obtained by combining the product with cart id to create the cart items.
        is_cart_item_exists = CartItem.objects.filter(
            product=product, cart=cart
        ).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            # this will return the cart item objects.                                           #cart_item =
            # CartItem.objects.create(product=product, quantity=1, cart=cart)    # cart items are stored inside the
            # cart_item variable, in CartItem model manner. create function is used to create a new cart item object
            # existing variations  -> from the database
            # current variations  -> product variation list from above
            # item id              -> from database
            # check for current variations inside the existing variations > increase the quantity of the cart item.
            id = []
            ex_var_list = []
            # created an empty list to store the variations
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            if product_variation in ex_var_list:
                # increase the item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variation.clear()  #
                    item.variations.add(*product_variation)
                    # cart_item.quantity += 1                                        # it is commented because it is
                    # added above # to count the number of items in the cart.
                    item.save()
                    # save the cart item to the database
                    # print('\n new item added to the cart\n\n')
        else:
            # CartItem.DoesNotExist:                                       #if cart item is empty.
            cart_item = (
                CartItem.objects.create(  # things need to create a new cart are these
                    product=product,
                    quantity=1,
                    cart=cart,
                )
            )
            if len(product_variation) > 0:
                cart_item.variation.clear()  #
                cart_item.variations.add(*product_variation)
            cart_item.save()
            # save the cart item to the database
            # print('\n\n items are added to the cart ')
            # return HttpResponse(cart_item.product)
            # exit()
        return redirect("view_cart")


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    # Product model, product id
    try:
        if (
            request.user.is_authenticated
        ):  # logged users are identified with their username.
            cart_item = CartItem.objects.get(
                product=product, user=request.user, id=cart_item_id
            )
        else:  # for guest users we use their session id to create them a cart for them
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(
                product=product, cart=cart, id=cart_item_id
            )
            # looking for these variable in the database
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect("view_cart")


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(
        Product, id=product_id
    )  # find the actual product with it's id.
    if (
        request.user.is_authenticated
    ):  # if authenticated we can get cart item by this query
        cart_item = CartItem.objects.get(
            product=product, user=request.user, id=cart_item_id
        )
    else:
        cart = Cart.objects.get(
            cart_id=_cart_id(request)
        )  # this query can be used to both create,
        # and find the cart of guest users
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        # here we use cart instead of users
    cart_item.delete()
    return redirect("view_cart")


# order
@login_required(login_url="otp_user_login")
def checkout(request, total=0, quantity=0, cart_items=None):
    # this checkout is simply a copy of the cart.
    tax = 0
    grand_total = 0
    discount = 0

    if "coupon_code" in request.session:
        print(request.session["coupon_code"])
        coupon = Coupon.objects.get(coupon_code=request.session["coupon_code"])
        discount = coupon.amount
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            # this will work for the guest users,
            cart = Cart.objects.get(cart_id=_cart_id(request))
            # calling the above private function for the cart id.
            # because the user is not logged in hence, he needs a cart id to keep cart items, which is created above.
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        # cart = Cart.objects.get(cart_id=_cart_id(request))  # calling the above private function for the cart id.
        # cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            # after this calculations we can add the offers based on these
            quantity = cart_item.quantity
            tax = (18 * total) / 100
            grand_total = total + tax

    except ObjectDoesNotExist:
        pass  # we can simply pass it.
    context = {
        "total": total + tax,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "grand_total": grand_total,
    }
    return render(request, "checkout.html", context)
    # return render(request, 'checkout.html', context)


def apply_coupon(request):
    # coupon_code = request.POST["coupon_code"]
    # print(coupon_code)
    # return HttpResponse(request)
    if request.method == "POST":
        coupon_code = request.POST.get("coupon_code")
        # coupon_code = request.POST['coupon']   what is the difference b/w two ?
        print(coupon_code)
        try:  # need to change this try except block
            if "coupon_code" in request.POST:
                print("coupon code is in request")
                if Coupon.objects.get(coupon_code=request.POST["coupon_code"]):
                    print("coupon matched")
                    coupon = Coupon.objects.get(coupon_code=request.POST["coupon_code"])
                    print("the current coupon code is ", coupon, coupon_code)
                    try:
                        if UsedCoupon.objects.get(user=request.user, coupon=coupon):
                            print("fail")
                            messages.warning(request, "Used Coupon")
                            return redirect(
                                "view_cart"
                            )  # need to chang the rerouting path
                    except:
                        print("pass")
                        request.session["coupon_code"] = request.POST["coupon_code"]
                        messages.success(request, "Coupon applied Successfully")
                        print(request.session["coupon_code"])
                        return redirect("view_cart")
            else:
                pass
        except:

            # print(request.session["coupon_code"])
            messages.error(request, "invalid Coupon ")
            return redirect("view_cart")
    else:
        pass
