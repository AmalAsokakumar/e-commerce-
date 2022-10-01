from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control
from .helper import sent_otp, check_otp

# email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# for importing, data to user account from the gust user mode
from store.models import Cart, CartItem
from store.views import _cart_id
from orders.models import Order, OrderProduct, Payment

# for dynamic searching import requests
import requests

#  for user Profile
from .models import UserProfile
from .forms import UserForm, UserProfileForm


# Create your views here.

# my questions are like what are the fields that these default django form have and how do i know them ?

# Create your views here.


def otp_register(request):
    # global phone_number  # in order make this variable globally available
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # to fetch the data from request
            request.session["first_name"] = form.cleaned_data["first_name"]
            request.session["last_name"] = form.cleaned_data["last_name"]
            request.session["email"] = form.cleaned_data["email"]
            request.session["phone_number"] = form.cleaned_data["phone_number"]
            request.session["password"] = form.cleaned_data["password"]
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            username = email.split("@")[0]
            request.session["username"] = username

            sent_otp(phone_number)
            return redirect("confirm")
    else:
        form = RegistrationForm()

    context = {
        "form": form,
    }
    return render(request, "register.html", context)  # template needed


def otp_confirm_signup(request):
    if request.user.is_authenticated:
        return redirect("/")
    elif request.method == "POST":
        otp = request.POST["otp_code"]
        print("the otp code is : " + str(otp))  # user inputted otp code
        phone_number = request.session["phone_number"]
        print(otp)
        if check_otp(phone_number, otp):
            first_name = request.session["first_name"]
            last_name = request.session["last_name"]
            email = request.session["email"]
            phone_number = request.session["phone_number"]
            password = request.session["password"]
            username = request.session["username"]

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                username=username,
            )
            user.phone_number = phone_number
            user.is_active = True
            user.save()
            # create user profile
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = "default/default-user.jpg"
            profile.save()
            return redirect("otp_user_login")  # redirect to login page
        else:
            print("OTP not matching")
            return redirect("confirm_signup")  # redirect to otp page
    return render(request, "otp_confirm.html")


def otp_sign_in(request):
    if request.user.is_authenticated:
        return redirect("/")
    elif request.method == "POST":
        phone_number = request.POST["phone_number"]
        try:
            if Account.objects.filter(phone_number=phone_number).first():
                sent_otp(phone_number)
                request.session["mobile"] = phone_number
                # __setitem__(phone_number, phone_number) # storing value temporarily in session
                return redirect("otp_check")  # reroute path not created
        except:
            messages.info(request, "User not registered")
            return redirect("register")
    return render(request, "otp.html", {})


def otp_check(request):
    if request.user.is_authenticated:
        return redirect("/")
    elif request.method == "POST":
        otp = request.POST["otp_code"]
        # if request.session.has_key["mobile"]:
        mobile = request.session["mobile"]
        # print('the section phone number is : ' + str(mobile))
        if_valid = check_otp(mobile, otp)
        # print('otp check : ' + str(if_valid))
        if if_valid:
            try:
                user = Account.objects.get(phone_number=mobile)
                # print(user.username, ' is authenticating... \n\n')
                cart = Cart.objects.get(
                    cart_id=_cart_id(request)
                )  # this query will get or create a new cart
                if cart is not None:
                    print("cart is not empty ", cart)
                is_cart_item_exist = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exist:
                    # print('cat is not empty \n', is_cart_item_exist)
                    cart_item = CartItem.objects.filter(cart=cart)
                    # print(cart_item)

                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass
            user = Account.objects.get(phone_number=mobile)
            auth.login(request, user)
            messages.info(request, "logged in Successfully")
            print("authenticated successfully")
            # dynamic routing started........................................................................
            url = request.META.get("HTTP_REFERER")
            try:
                query = requests.utils.urlparse(
                    url
                ).query  # query ->  next = / admin - home /
                # print('query -> ', query)
                params = dict(
                    x.split("=") for x in query.split("&")
                )  # param ->  {'next': '/admin-home/'}
                # print('params -> ', params)  # we need to redirect the user to this param path
                if "next" in params:
                    nextPage = params["next"]
                    return redirect(nextPage)
            except:
                print("executing the else block")
                return redirect("admin_home")
            # dynamic routing ended...........................................................................
        else:
            messages.info(request, "OTP not Valid")
            return redirect("otp_check")
    else:
        print(" error locating the phone number ")

    return render(request, "otp_confirm.html", {})


def resent_otp(request):
    mobile = request.session["phone_number"]
    sent_otp(mobile)
    return redirect("otp_check")


def forgot_password(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            phone_number = request.POST["phone_number"]
            if Account.objects.get(phone_number=phone_number):
                print("account details found")
                sent_otp(request.POST["phone_number"])
                request.session["phone_number"] = phone_number
                print("\n\n\n")
                return redirect("reset_password")
            else:
                messages.warning(request, "mobile number is not registered ")
                return redirect("register")
    return render(request, "forgot_password.html", {})


def reset_password(request):
    if request.user.is_authenticated:
        return redirect("/")
    elif request.method == "POST":
        otp = request.POST["otp_code"]
        password = request.POST["password"]
        if request.session["phone_number"]:
            phone_number = request.session["phone_number"]
            # if otp == '123456':
            #     print('otp_matched \n\n\n')
            if_valid = check_otp(phone_number, otp)
            if if_valid:  # check if it is true, then the following will be executed
                user = Account.objects.get(phone_number=phone_number)
                user.set_password(
                    password
                )  # through this we can actually store the hashed password for the user
                user.save()
                print(password)
                print("password changed \n\n")
                print(user.email)
                if user.check_password(
                    password
                ):  # check if the hashed password is matching or not not actually required
                    print("true")
                return redirect("dashboard")
            else:
                messages.warning(request, "invalid otp")
                return render(request, "otp_confirm.html", {})  # conform otp page
        # return redirect('forgot_password')
    return render(request, "reset_password.html", {})


# register function  with email activation . need more adjustments !!! in email or server side

# staff user https://www.youtube.com/watch?v=uVDq4VOBMNM&t=81s  partially completed need further alternation on the
# gmail part and do the authorization part
def register(request):
    if request.method == "POST":
        form = RegistrationForm(
            request.POST
        )  # here the request.post will contain all the field values from the
        # form submission.
        if (
            form.is_valid()
        ):  # to check whether all the field in this form is valid or not.
            if Account.objects.filter(email=form.cleaned_data["email"]):
                messages.error(request, "email id  already exist")
            else:
                first_name = form.cleaned_data[
                    "first_name"
                ]  # while using django forms we use cleaned_data to fetch
                # the values/from request
                last_name = form.cleaned_data["last_name"]
                email = form.cleaned_data["email"]
                phone_number = form.cleaned_data["phone_number"]
                password = form.cleaned_data["password"]
                # we will validate to conform password with password in form level only.
                username = email.split("@")[
                    0
                ]  # here we are using first part of email to create a username for the
                # user.

                # to create a user, here the create_user is from django  models we have create_user in MyAccountManager,
                # similarly there is a function to create a superuser also.
                user = Account.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    username=username,
                )  # there is no field to accept phone number in models.py, so we are
                # attaching it like.
                if Account.objects.filter(
                    phone_number=form.cleaned_data["phone_number"]
                ):
                    messages.error(request, "email id already taken")
                else:
                    user.phone_number = phone_number  # this will update the user object with the phone number.
                # user.is_active = True
                # user.is_staff = True
                user.save()  # this field will be created in the database.

                # user activations
                current_site = get_current_site(
                    request
                )  # to get the current site details
                mail_subject = "Please activate your account"
                # this is the actual message that we wanted to send, rather than sending one we are actually sending
                # a template.
                message = render_to_string(
                    "accounts/account_verification_email.html",
                    {
                        "user": user,
                        "domain": current_site,
                        "uid": urlsafe_base64_encode(
                            force_bytes(user.pk)
                        ),  # here we are
                        # actually encoding the user id with this base64 so that no one can
                        # access that. we will decode it later when we activate it
                        "token": default_token_generator.make_token(
                            user
                        ),  # first part is the
                        # library and the second part .make_token is the function that is
                        # going to make the token, then we pass the user because we are
                        # actually making the token for the user
                    },
                )
                to_email = email  # user's email address which we obtained at the time of signup.
                # messages.success(request, 'Registration success ')
                send_email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )  # to email can be multiple
                send_email.send()  # we need to configure the email to send the email datas
                return render(request, "register.html", {})

    else:
        form = RegistrationForm()
    context = {
        "form": form,
    }
    return render(request, "register.html", context)


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
def activate(request):
    pass


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    # if 'email' in request.session:
    # return redirect('admin_home')

    if request.user.is_authenticated:
        return redirect("admin_home")  # create a templated to handle this

    elif request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        print("email, password ", (email, password))
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                print(user.username, " is authenticating... \n\n")
                cart = Cart.objects.get(cart_id=_cart_id(request))
                if cart is not None:
                    print("cart is not empty ", cart)
                is_cart_item_exist = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exist:
                    print("cat is not empty \n", is_cart_item_exist)
                    cart_item = CartItem.objects.filter(cart=cart)
                    print(cart_item)
                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass
            print(user.username)
            auth.login(request, user)
            # print('\n\n user is authenticated ')
            # request.session['email']= email
            # dynamic routing started........................................................................
            url = request.META.get("HTTP_REFERER")
            try:
                query = requests.utils.urlparse(
                    url
                ).query  # query ->  next = / admin - home /
                print("query -> ", query)
                params = dict(
                    x.split("=") for x in query.split("&")
                )  # param ->  {'next': '/admin-home/'}
                print(
                    "params -> ", params
                )  # we need to redirect the user to this param path
                if "next" in params:
                    nextPage = params["next"]
                    return redirect(nextPage)
            except:
                print("executing the else block")
                return redirect("admin_home")
            # dynamic routing ended...........................................................................
        else:
            messages.error(request, "Invalid username or password")
            print("invalid credentials ")
            return redirect("/")
    else:
        context = {}
    return render(request, "login.html", {})


# @login_required(login_url="otp_user_login")
def logout(request):
    auth.logout(request)
    messages.success(request, "you are logged out")
    return redirect("login")


@login_required(login_url="login")
def change_password(request):
    if request.method == "POST":
        # current_password = request.POST["current_password"]
        current_password = request.POST["current_password"]
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]
        user = Account.objects.get(username__exact=request.user.username)
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password updated successfully ")
                return redirect("change_password")
            else:
                messages.error(request, "please enter valid password")
        else:
            messages.error(request, "password doesn't match")
            return redirect("change_password")
    return render(request, "change_password.html", {})


# admin side
def admin_list_users(request):  # need to recheck this
    # list= Account.objects.order_by('id')
    lists = Account.objects.filter(is_superuser=False).order_by("id")

    context = {
        "list": lists,
    }
    return render(request, "list_users.html", context)


def admin_user_enable(request, id):
    user = Account.objects.get(pk=id)
    user.is_active = True
    user.save()
    return redirect("admin_list_users")


def admin_user_block(request, id):
    user = Account.objects.get(pk=id)
    user.is_active = False
    user.save()
    return redirect("admin_list_users")


@login_required(login_url="admin_login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_home(request):
    # if 'email' in request.session:
    # return HttpResponse('home view')
    # return render(request, 'sneat/admin_index.html', {}) # for testing temp hide it
    return render(request, "admin_index.html", {})


def admin_list_orders(request):
    orders = Order.objects.filter(is_ordered=True).order_by(
        "-created_at"
    )  # result will be printed in  descending order because we use a hype.
    context = {
        "orders": orders,
    }
    return render(request, "admin_list_users.html", context)


# user side
@login_required(login_url="otp_user_login")
def dashboard(request):
    orders = Order.objects.order_by("-created_at").filter(
        user_id=request.user.id, is_ordered=True
    )
    orders_count = orders.count()
    print(orders_count, "\n\n")
    context = {
        "orders_count": orders_count,
    }
    return render(request, "dashboard.html", context)


@login_required(login_url="otp_user_login")
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by(
        "-created_at"
    )  # result will be printed in  descending order because we use a hype.
    context = {
        "orders": orders,
    }
    return render(request, "my_orders.html", context)


@login_required(login_url="otp_user_login")
def edit_profile(request):
    user_profile = get_object_or_404(
        UserProfile, user=request.user
    )  # it will fetch the user profile if one
    # exist if not it will shows 404 error
    print(user_profile)
    if request.method == "POST":  # we are using two form to handel it
        user_form = UserForm(  # we are updating the first part of the profile
            request.POST, instance=request.user
        )  # here we are actually using an instance because we are actually editing a user instance.
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile
        )  # request.File is used to fetch the profile picture of the user and edit it properly.
        #  here we don't have a existing user instance hence we need to edit it by ourselves.
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "your profile has been updated")
            return redirect("edit_profile")
    else:
        user_form = UserForm(
            instance=request.user
        )  # by passing the instance we can see the data in the existing form
        profile_form = UserProfileForm(instance=user_profile)
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "user_profile": user_profile,
    }
    return render(request, "edit_profile.html", context)


@login_required(login_url="otp_user_login")
def view_order_(request, id):
    # print(id, "\n\n\n")
    # a = "00" + str(id)
    # print("/n/n/n", a)
    ordered_products = OrderProduct.objects.filter(order__order_number=id)
    order = Order.objects.get(order_number=id)
    sub_total = 0
    for i in ordered_products:
        sub_total += i.product_price * i.quantity
    # payment = Payment.objects.get(user=request.user)
    # print(id, "order", order)
    context = {
        "order": order,
        "ordered_products": ordered_products,
        # "order_number": order.order_number,
        # "transID": payment.payment_id,
        # "payment": order.payment,
        "order_detail": order,
        "sub_total": sub_total,
    }
    return render(request, "order_complete.html", context)


def cancel_order(request, order_number):
    print(order_number)
    order = Order.objects.get(user=request.user, order_number=order_number)
    print(order)
    order_products = OrderProduct.objects.filter(
        order__order_number=order_number
    )  # order.order_number=order_number
    print(order_products)
    order.status = "Canceled"
    order.save()
    for order_product in order_products:
        order_product.product.stock += order_product.quantity
        order_product.product.save()

    return redirect("my_orders")


# needed further editing on the cod payment.
# def cod_payment(request, order_number):
#     pass
#     print(order_number, "\n\n")
#     order = Order.objects.get(
#         user=request.user, is_ordered=False, order_number=order_number
#     )
#     print(order, "ordered list \n")
#     payment = Payment(
#         user=request.user,
#         payment_method="cash on delivery",
#         amount_paid=order.order_total,
#         status="pending",
#     )
#     payment.save()
#     order.is_ordered = True
#     # updating the order foreign key filed
#     order.payment = payment
#     order.satus = "Pending"
#     order.save()
#     cart_items = CartItem.objects.filter(user=request.user)
#     for items in cart_items:
#         order_product = OrderProduct()
#         # print(order_id, "\n\n\n")
#         order_product.order.id = order.id  # same for all the products
#         order_product.product_price = (
#             item.product.price
#         )  # product price is fetched from the foreign key of OrderProduct Model.
#         order_product.ordered = True
#         order_product.save()  # saving the products one by one.
#         cart_item = CartItem.objects.get(id=item.id)
#         product_variation = cart_item.variations.all()  # getting all variations
#         order_product = OrderProduct.objects.get(
#             id=order_product.id
#         )  # filtering the product based on
#         orderproduct.variations.set(product_variation)
#         order_product.save()
#         #  reduce the quantity of the ordered product for the stock
#         product = Product.objects.get(id=item.product_id)
#         product.stock -= item.quantity
#         product.save()
#     #  after ordering clearing the cart items.
#     CartItem.objects.filter(user=request.user).delete()
#     order = Order.objects.get(order_number=order_number, is_ordered=True)
#     order_product = OrderProduct.objects.filter(order_id=order.id)
#     for i in order_product:
#         sub_total = i.product_price * i.quantity
#     context = {
#         "order": order,
#         "order_products": order_products,
#         "order_number": order.order_number,
#     }
#     return render(request, "cod.html", context)
