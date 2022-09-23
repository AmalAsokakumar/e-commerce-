from twilio.rest import Client
# for environ variable
from ecommerce.settings import env


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
def sent_otp(mobile):
    phone = "+91" + str(mobile)
    account_sid = env('account_sid')
    auth_token = env('auth_token')
    client = Client(account_sid, auth_token)

    verification = client.verify.services(
        env('V_ID')
    ).verifications.create(to=phone, channel="sms")

    print(verification.status)


def check_otp(mobile, otp):
    account_sid = env('account_sid')
    auth_token = env('auth_token')
    client = Client(account_sid, auth_token)

    verification_check = client.verify.services(
        env('V_ID')
    ).verification_checks.create(to="+91" + mobile, code=otp)

    print(verification_check.status)
    if verification_check.status == "approved":
        return True
    else:
        return False
