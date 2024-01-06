import requests
import sys
from package.token_utils import get_codararc_value, decode_token
from package.config import config


def check_user_subscription_status(user_email):
    headers = {
        'Authorization': f'Bearer {get_codararc_value("access_token")}'
    }
    subscription = requests.get(f"{config.get('api_domain')}/api/user/subscription/grantAccess", params={'email': user_email},
                                headers=headers)

    if subscription.status_code == 200:
        return subscription.json().get('grantAccess')
    else:
        print(f'User subscription issue, error: {subscription.json()["errorMessage"]}')
        sys.exit(1)


def check_if_user_exists(user_email):
    headers = {
        'Authorization': f'Bearer {get_codararc_value("access_token")}'
    }
    try:
        response = requests.get(f"{config.get('api_domain')}/api/user", params={'email': user_email}, headers=headers)
        if response.status_code == 200:
            return True
        return False
    except Exception as e:
        print(f'Error checking if user exists: {e}')
        sys.exit(1)


def create_user(user_email):
    headers = {
        'Authorization': f'Bearer {get_codararc_value("access_token")}'
    }
    try:
        response = requests.post(f"{config.get('api_domain')}/api/user/create", json={'email': user_email}, headers=headers)
        if response.status_code == 201:
            print('User created successfully')
            return response.json()
    except Exception as e:
        print(f'Error creating a user: {e}')
        sys.exit(1)


def check_if_user_exists_or_create():
    user_email = decode_token(get_codararc_value('id_token')).get('email')
    try:
        if not check_if_user_exists(user_email):
            return create_user(user_email)
    except Exception as e:
        print(f'Error checking if user exists: {e}')
        sys.exit(1)
