import os
import webbrowser
import sys
import requests
from datetime import datetime, timezone
from package.server import app, start_tornado, stop_tornado, check_for_signal_file
from package.token_utils import decode_token, is_token_valid, get_codararc_value, replace_token_in_file
from package.config import config


def initiate_login():
    login_url = config.get('aws_hosted_ui_domain')
    webbrowser.open(login_url)


def access_token_expired():
    raw_access_token = get_codararc_value('access_token')

    if not raw_access_token:
        print("Access token not found, please login again.")
        return True

    access_token = decode_token(get_codararc_value('access_token'))
    access_token_expiry = access_token.get('exp')
    utc_now = datetime.now(timezone.utc)
    current_date_utc = int(utc_now.timestamp())

    if not access_token_expiry:
        print("Access token expiration not found, please login again.")
        return True

    if access_token_expiry < current_date_utc:
        return True
    else:
        return False


# def refresh_token_expired():
#     print('****started******refresh_token_expired')
#     refresh_token = decode_token(get_codararc_value('refresh_token'))
#     print('****end******refresh_token_expired')
#     # Convert Unix timestamp to datetime object
#     print('***refresh', refresh_token)
#     refresh_token_expiry = refresh_token.get('exp')
#     # Get current datetime in UTC
#     current_date_utc = datetime.utcnow()
#     if refresh_token_expiry:
#         if refresh_token_expiry < current_date_utc.timestamp():
#             return True
#         else:
#             return False
#     else:
#         print("Refresh token not found, please login again.")
#         return False


def get_new_access_token():
    token_file_path = os.path.join(os.path.expanduser("~"), '.codararc')
    refresh_token = get_codararc_value('refresh_token')

    if not refresh_token:
        print("Refresh token not found, please login again.")
        if token_file_path:
            os.remove(token_file_path)
        sys.exit(1)

    response = requests.post(f"{config.get('api_domain')}/api/auth/refresh-token", json={"refreshToken": refresh_token})
    if response.status_code == 200 or response.status_code == 201:
        response_data = response.json()
        access_token = response_data.get('accessToken')
        id_token = response_data.get('idToken')
        if access_token and id_token:
            replace_token_in_file('access_token', access_token)
            replace_token_in_file('id_token', id_token)
        else:
            raise Exception("Error: Access token not found in response")
    else:
        if token_file_path:
            os.remove(token_file_path)
        raise Exception(f"{response.status_code} Error in get_new_access_token: {response.json()['errorMessage']}, please login again.")


def login(port=54371):
    if os.path.exists(os.path.expanduser('~/.codararc')):
        id_token = decode_token(get_codararc_value('id_token'))
        access_token = decode_token(get_codararc_value('access_token'))
        logged_in_message = 'you are logged in'

        if not id_token.get('email_verified'):
            print("Email not verified, please check your email and verify your account.")
            sys.exit(1)

        if access_token and is_token_valid(access_token):
            print(logged_in_message)
        else:
            try:
                get_new_access_token()
                print(logged_in_message)
            except Exception as e:
                print(f"Error: {e}")
                sys.exit(1)
    else:
        # Start the Gunicorn server
        tornado_server, tornado_thread = start_tornado(port)

        # Open the web browser for user login
        initiate_login()

        # Wait for the authentication to complete (check for the signal file)
        check_for_signal_file()

        # Stop the Gunicorn server after the process is complete
        stop_tornado(tornado_server, tornado_thread)
