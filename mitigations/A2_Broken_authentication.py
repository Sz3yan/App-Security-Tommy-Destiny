from twilio.rest import Client
import random

def getOTPTwilio(phno):
    twilio_account_sid = 'ACa38acb2c03e6b35c1bd7ba00fbdcd1a2'
    twilio_auth_token = '5cce5cb9b1b2aaea8db39e183ff24629'
    client = Client(twilio_account_sid, twilio_auth_token)
    otp = random.randrange(100000,999999)
    body = 'Your OTP is ' + str(otp)
    message = client.messages.create(from_='+16506681171', body=body, to=phno)

    if message.sid:
        return otp
    else:
        return ""