import os
from decouple import config
import requests
import random

def bkash_genarate_token(id):
    url = config("bkash_grant_token_url")
    payload = {
        "app_key": config("bkash_api_key"),
        "app_secret": config("bkash_app_secret_key")
    }
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "username": config("bkash_username"),
        "password": config("bkash_password")
    }

    response = requests.post(url=url, json=payload, headers=headers)

    if response.status_code == 200:
        try:
            # Parse the response as JSON
            response_data = response.json()
            # Print the 'id_token' from the response
            id_token = response_data.get('id_token')
            if id_token:
                return id_token
            else:
                print("ID token not found in the response")
        except ValueError:
            # Handle the case where the response isn't JSON
            print("Response is not in JSON format")
            print(response.json)
    else:
        print(f"Error: {response.status_code}")
        print(response.json)


def bkash_create_payment(id, amount , callback_url):
    url = config("bkash_create_url")
    
    # Retrieve the base URL first, then concatenate with the endpoint
    
    payload = {
        "mode": "0011",
        "payerReference": " ",
        "callbackURL": callback_url,
        "amount": amount,
        "currency": "BDT",
        "intent": "sale",
        "merchantInvoiceNumber": "ADADA" + str(random.randint(1, 100000))
    }

    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": id,
        "x-app-key": config("bkash_api_key")
    }

    response = requests.post(url=url, json=payload, headers=headers)
    
    if response.status_code == 200:
        try:
            # Parse the response as JSON
            response_data = response.json()
            bkash_url = response_data.get('bkashURL')
            if bkash_url:
                return bkash_url
            else:
                print("ID token not found in the response")

            print(response_data)
        except ValueError:
            # Handle the case where the response isn't JSON
            print("Response is not in JSON format")
            print(response.json())
    else:
        print(f"Error: {response.status_code}")
        print(response.json())


def bkash_execute_payment(token,payment_id):
    url = config("bkash_execute_url")
    
    payload = {
        "paymentID": payment_id
    }

    headers = {
        "Accept": "application/json",
        "Authorization": token,  # Using the token passed in the callback
        "x-app-key": config("bkash_api_key")
    }

    response = requests.post(url=url, json=payload, headers=headers)
    
    if response.status_code == 200:
        try:
            return response.json()  # Handle and return the actual response
        except ValueError:
            print("Response is not in JSON format")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None
