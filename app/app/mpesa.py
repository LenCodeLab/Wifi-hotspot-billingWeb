import requests
import base64
import datetime
import os

def get_access_token():
    consumer_key = os.getenv('MPESA_CONSUMER_KEY')
    consumer_secret = os.getenv('MPESA_CONSUMER_SECRET')
    auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(auth_url, auth=(consumer_key, consumer_secret))
    return response.json().get('access_token')

def lipa_na_mpesa_online(phone, amount):
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    shortcode = os.getenv('MPESA_SHORTCODE')
    passkey = os.getenv('MPESA_PASSKEY')
    callback_url = os.getenv('MPESA_CALLBACK_URL')

    password = base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": callback_url,
        "AccountReference": "FlaskM-Pesa",
        "TransactionDesc": "Payment"
    }

    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
