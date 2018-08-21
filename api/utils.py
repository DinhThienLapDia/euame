from mailjet_rest import Client

from twilio.rest import Client as Twilio

def send_email(content):
    api_key = 'a0447053ba64e12d58c6f18ee42bcfc5'
    api_secret = '03d7d5b3791148902dcffd64edb62dbb'
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')

    return mailjet

def send_sms(phone_number,content):
    account_sid = 'AC4d3a68850fdbae49d26518b29c1e0404'
    auth_token = '65890d206e6755cf15afc2b3b5e6c0ee'
    client = Twilio(account_sid, auth_token)

    message = client.messages.create(
                              body=content,
                              from_='+12243081374',
                              to=phone_number
                          )