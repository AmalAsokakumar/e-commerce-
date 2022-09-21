import os
from twilio.rest import Client
from django.conf import settings


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
def sent_otp(mobile):
    phone = "+91" + str(mobile)
    account_sid = 'ACc660ccef21cee4623d91ae2cd22fb931'
    auth_token = '3fe080b67230b708089f613201464b66'
    client = Client(account_sid, auth_token)

    verification = client.verify.services(
        'VA51e9f2ecb5d8db68a4dcfa95b6ed53a1'
    ).verifications.create(to=phone, channel="sms")

    print(verification.status)


def check_otp(mobile, otp):
    account_sid = 'ACc660ccef21cee4623d91ae2cd22fb931'
    auth_token = '3fe080b67230b708089f613201464b66'
    client = Client(account_sid, auth_token)

    verification_check = client.verify.services(
        'VA51e9f2ecb5d8db68a4dcfa95b6ed53a1'
    ).verification_checks.create(to="+91" + mobile, code=otp)

    print(verification_check.status)
    if verification_check.status == "approved":
        return True
    else:
        return False
