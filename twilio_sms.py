from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token  = os.environ.get('TWILIO_AUTH_TOKEN')
phone_number = os.environ.get('TWILIO_PHONE_NUMBER')

print(account_sid)
print(auth_token)
print(phone_number)

client = Client(account_sid, auth_token)


def send_sms(user_phone_number, otp):    
    message = client.messages.create(
            to=user_phone_number,
            from_=phone_number,
            body=f"Your Phone number verification code is {otp}")
    
    print(message.sid)
