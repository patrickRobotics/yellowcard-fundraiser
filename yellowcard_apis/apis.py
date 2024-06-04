from typing import Dict
import json
import requests
import hmac
import hashlib
from datetime import datetime
import base64
from urllib.parse import urlencode, urlunparse
import os
from dotenv import load_dotenv

load_dotenv()

base_url = "sandbox.api.yellowcard.io"

api_key = os.getenv('API_KEY')
api_secret = os.getenv('SECRET_KEY')
if isinstance(api_secret, str):
    api_secret_bytes = api_secret.encode('utf-8')
else:
    raise TypeError("SECRET_KEY is not a valid string")


def yellow_card_req_auth(request_path: str, method: str, body=None) -> Dict[str, str]:
    date_time = datetime.utcnow().isoformat() + "Z"
    hmac_object = hmac.new(key=api_secret_bytes, digestmod=hashlib.sha256)
    if method == "GET":
        message = f"{date_time}{request_path}{method}"
        # Update the HMAC with the message
        hmac_object.update(message.encode('utf-8'))

    if method == "POST" or method == "PUT":
        hmac_object.update(date_time.encode('utf-8'))
        hmac_object.update(request_path.encode('utf-8'))
        hmac_object.update(method.encode('utf-8'))

        body_json = json.dumps(body)
        body_bytes = body_json.encode('utf-8')
        body_hmac = base64.b64encode(hashlib.sha256(body_bytes).digest()).decode('utf-8')
        hmac_object.update(body_hmac.encode('utf-8'))

    signature = base64.b64encode(hmac_object.digest()).decode('utf-8')
    # Prepare headers
    headers = {
        'X-YC-Timestamp': date_time,
        'Authorization': f'YcHmacV1 {api_key}:{signature}'
    }
    return headers


def create_url(path: str, **kwargs: [str, str]) -> str:
    """
    Creates a URL with optional query parameters.

    Parameters:
    base_url (str): The base URL.
    path (str): The path to append to the base URL.
    Kwargs list of optional parameters like:
        country (str, optional): The country parameter. Defaults to None.
        status (str, optional): The status parameter. Defaults to None.

    Returns:
    str: The constructed URL.
    """
    query_params = {}
    if kwargs is not None:
        for key, value in kwargs.items():
            query_params[key] = value

    query_string = urlencode(query_params)
    url_parts = ('https', base_url, path, '', query_string, '')

    return urlunparse(url_parts)


def post_collection_request(method: str, request_path: str, payload: dict) -> Dict[str, str]:
    url = create_url(request_path)
    headers = yellow_card_req_auth(request_path, method, body=payload)
    try:
        response = requests.post(url, data=payload, headers=headers)
        print(f"Response Status Code: {response.status_code}")

        if response.status_code // 100 == 2:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            response.raise_for_status()

    except Exception as e:
        print(f"An error occurred: {e}")


def get_yellow_card_channels(method: str, request_path: str, country: str = None, status: str = None) -> Dict[str, str]:
    url = create_url(request_path, country=country, status=status)
    headers = yellow_card_req_auth(request_path, method)
    try:
        # Make the GET request
        response = requests.get(url, headers=headers)
        print(f"Response Status Code: {response.status_code}")

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    except Exception as e:
        print(f"An error occurred: {e}")


def get_yellow_card_networks(method: str, request_path: str) -> Dict[str, str]:
    url = create_url(request_path)
    headers = yellow_card_req_auth(request_path, method)
    try:
        # Make the GET request
        response = requests.get(url, headers=headers)
        print(f"Response Status Code: {response.status_code}")

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    except Exception as e:
        print(f"An error occurred: {e}")


def get_yellowcard_accounts(method: str, request_path: str):
    url = create_url(request_path)
    headers = yellow_card_req_auth(request_path, method)

    try:
        response = requests.get(url, headers=headers)
        print(f"Response Status Code: {response.status_code}")

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    except Exception as e:
        print(f"An error occurred: {e}")


def get_yellowcard_rates(method: str, request_path: str, country_code: str = None) -> Dict[str, str]:
    url = create_url(request_path, locale=country_code)
    headers = yellow_card_req_auth(request_path, method)

    try:
        response = requests.get(url, headers=headers)
        print(f"Response Status Code: {response.status_code}")

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    except Exception as e:
        print(f"An error occurred: {e}")


def post_yellow_card_webhook(method: str, request_path: str, payload: Dict[str, str]):
    url = create_url(request_path)
    headers = yellow_card_req_auth(request_path, method, payload)

    try:
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code // 100 == 2:
            print("API Response:")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"An error occurred: {e}")


#channels = get_yellow_card_channels("GET", "/business/channels", country="UG")


#accounts = get_yellowcard_accounts("GET", "/business/account")

#rates = get_yellowcard_rates("GET", "/business/rates")


body = {
    "active": True,
    "url": "https://test.sample.com/webhook/test",
    "state": "collection.complete"
}
#res = post_yellow_card_webhook("POST", "/webhook/test", payload=body)


