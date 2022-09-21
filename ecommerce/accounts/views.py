from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control
from .helper import sent_otp, check_otp


# Create your views here.

# my questions are like what are the fields that these default django form have and how do i know them ?

# Create your views here.

def otp_register(request):
    # global phone_number  # in order make this variable globally available
    if request.user.is_authenticated:
        return redirect('homepage')
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
            return redirect('confirm')
    else:
        form = RegistrationForm()

    context = {
        "form": form,
    }
    return render(request, "register.html", context)  # template needed


def otp_confirm_signup(request):
    if request.user.is_authenticated:
        return redirect("homepage")
    if request.method == "POST":
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
            user.save()

            return redirect("otp_user_login")  # redirect to login page
        else:
            print("OTP not matching")
            return redirect("confirm_signup")  # redirect to otp page
    return render(request, "otp_confirm.html")


def otp_sign_in(request):

    if request.method == "POST":
        phone_number = request.POST["phone_number"]
        try:
            if Account.objects.filter(phone_number=phone_number).first():
                sent_otp(phone_number)
                request.session["phone_number"] = phone_number
                # __setitem__(phone_number, phone_number) # storing value temporarily in session
                return redirect("otp_check")  # reroute path not created
        except:
            messages.info(request, "User not registered")
            return redirect("otp_register")
    return render(request, "otp.html", {})


def otp_check(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        otp = request.POST["otp_code"]
        mobile = request.session["phone_number"]
        if_valid = check_otp(mobile, otp)
        if if_valid:
            user = Account.objects.get(phone_number=mobile)
            auth.login(request, user)
            messages.info(request, "Authenticated Successfully")
            return redirect("Homepage")

        else:
            messages.info(request, "OTP not Valid")
            return redirect("otp_check")

    return render(request, "otp_confirm.html", {})


def resent_otp(request):
    mobile = request.session["phone_number"]
    sent_otp(mobile)
    return redirect("otp_check")


# register function  with out any otp method for activation. need more adjustments


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(
            request.POST)  # here the request.post will contain all the field values from the form submission.

        if form.is_valid():  # to check whether all the field in this form is valid or not.
            first_name = form.cleaned_data[
                'first_name']  # while using django forms we use cleaned_data to fetch the values/from request
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data[
                'password']  # we will validate the conform password with password in form level only.
            username = email.split('@')[0]  # here we are using first part of email to create a username for the user.

            # to create a user, here the create_user is from django  models we have create_user in MyAccountManager,
            # similarly there is a function to create a super user also.
            user = Account.objects.create_user(first_name=first_name,
                                               last_name=last_name,
                                               email=email,
                                               password=password,
                                               username=username
                                               )  # there is no field to accept phone number in models.py so we are
            # attaching it like.
            user.phone_number = phone_number  # this will update the user object with the phone number.
            user.save()  # this field will be created in the database.
            return render(request, 'login.html', {})

    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    # if 'email' in request.session:
    # return redirect('admin_home')

    if request.user.is_authenticated:
        return redirect('/')  # create a templated to handle this

    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            # request.session['email']= email

            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('/')
    else:
        context = {}
    return render(request, 'login.html', {})


# repeated functions are needed.

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'you are logged out')
    return redirect('admin_login')
