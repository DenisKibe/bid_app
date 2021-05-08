from threading import Thread
import requests
from app import app

headers = {'ContentType':'application/Json'}
data = {
    'SenderId': app.config['CLIENTID'],
    'ApiKey': app.config['APIKET'],
    'ClientId': app.config['SENDER_ID'],
    'Message' : '',
    'MobileNumbers' : ''
}

def send_async_sms(app, data):
    global headers
    with app.app_context():
        try:
            requests.post('http://sms.websms.co.ke:6005/api/v2/SendSMS', data=data , headers=headers)

        except Exception as e:
            raise SystemError('BulkSms Services experincing a problem')

def SendSms(message, phoneNumber):
    global data

    data['Message'] = message
    data['MobileNumbers'] = phoneNumber

    Thread(target=send_async_sms, args=(app, data)).start()



