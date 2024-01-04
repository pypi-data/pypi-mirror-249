import jwt
import os
import sys
from datetime import datetime, timezone


def save_tokens_to_file(key, value):
    token_file_path = os.path.join(os.path.expanduser("~"), '.codararc')
    with open(token_file_path, 'a') as token_file:
        token_file.write(f'{key}={value}\n')


def replace_token_in_file(key, new_value):
    token_file_path = os.path.join(os.path.expanduser("~"), '.codararc')
    content_updated = False
    updated_lines = []

    if not os.path.exists(token_file_path):
        print(f'File {token_file_path} not found')
        sys.exit(1)

    # Read the file and replace the value for the given key
    with open(token_file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith(f'{key}='):
            updated_lines.append(f'{key}={new_value}\n')
            content_updated = True
        else:
            updated_lines.append(line)

    # Write the updated content back, or append the new key-value if key wasn't found
    with open(token_file_path, 'w') as file:
        file.writelines(updated_lines)
        if not content_updated:
            file.write(f'{key}={new_value}\n')


def get_codararc_value(key):
    token_file_path = os.path.join(os.path.expanduser("~"), '.codararc')
    if not os.path.exists(token_file_path):
        print(f'Please login again.')
        sys.exit(1)
    try:
        with open(token_file_path, 'r') as token_file:
            for line in token_file:
                if line.startswith(key + '='):
                    return line.strip().split('=')[1]
    except Exception as e:
        raise Exception(f'Error reading {key} from {token_file_path}. Exception: {e}')


def decode_token(token):
    """Decodes the JWT token and returns the decoded payload."""
    try:
        return jwt.decode(token, options={"verify_signature": False})
    except jwt.ExpiredSignatureError:
        raise Exception('Token expired, please login again')
    except jwt.InvalidTokenError:
        raise Exception('Invalid Token, please login again')


def read_token_from_file():
    """Reads the JWT token from the ~/.codararc file."""
    token_file_path = os.path.join(os.path.expanduser("~"), '.codararc')

    if not os.path.exists(token_file_path):
        raise FileNotFoundError(f'File {token_file_path} not found')

    if os.path.exists(token_file_path):
        with open(token_file_path, 'r') as file:
            return file.read().strip()


def is_token_valid(token):
    """Decodes the JWT token and checks if it's still valid with an additional grace period."""
    if not 'exp' in token:
        print('Token does not contain an expiration date')
        return False
    try:
        expiration_time = token.get('exp')
        utc_now = datetime.now(timezone.utc)
        current_time = int(utc_now.timestamp())

        return expiration_time > current_time
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
