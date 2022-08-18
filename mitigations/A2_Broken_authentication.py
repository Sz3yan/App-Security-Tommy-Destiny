import random

from mitigations.A3_Sensitive_data_exposure import GoogleSecretManager
from twilio.rest import Client


googlesecretmanager = GoogleSecretManager()

twilio_account_sid = googlesecretmanager.get_secret_payload("tommy-destiny", "twilio_account_sid", "1")
twilio_auth_token = googlesecretmanager.get_secret_payload("tommy-destiny", "twilio_auth_token", "1")

def getOTPTwilio(phno):
    client = Client(twilio_account_sid, twilio_auth_token)
    otp = random.randrange(100000,999999)
    body = 'Your OTP is ' + str(otp)
    message = client.messages.create(from_='+16506681171', body=body, to=phno)

    if message.sid:
        return otp
    else:
        return ""