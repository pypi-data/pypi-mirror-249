import subprocess
import os
from flask import Flask, request, jsonify
import requests
import time
import tornado.wsgi
import tornado.httpserver
import tornado.ioloop
import threading
from package.utils import print_codara_ascii_message
from package.token_utils import save_tokens_to_file
from package.config import config

app = Flask(__name__)


def start_tornado(port):
    """Start Tornado server with the Flask app."""
    container = tornado.wsgi.WSGIContainer(app)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(port)

    # Start the I/O loop in a separate thread
    tornado_thread = threading.Thread(target=tornado.ioloop.IOLoop.instance().start)
    tornado_thread.start()
    return http_server, tornado_thread

def stop_tornado(http_server, tornado_thread):
    """Stop Tornado server."""
    http_server.stop()
    tornado.ioloop.IOLoop.instance().stop()
    tornado_thread.join()


def start_gunicorn(app_module, port):
    """Start Gunicorn server with the Flask app."""
    return subprocess.Popen(['gunicorn', '-b', f'localhost:{port}', '-w', '1', app_module])


def stop_gunicorn(gunicorn_process):
    """Stop Gunicorn server."""
    gunicorn_process.terminate()


def signal_authentication_complete():
    signal_file_path = os.path.join(os.getcwd(), 'auth_complete')
    with open(signal_file_path, 'w') as file:
        file.write('complete')


def check_for_signal_file():
    signal_file_path = os.path.join(os.getcwd(), 'auth_complete')
    while not os.path.exists(signal_file_path):
        time.sleep(1)  # Check every second for the authentication signal
    time.sleep(1)  # Slight delay for graceful completion
    os.remove(signal_file_path)
    print_codara_ascii_message()


def start_flask_app():
    app.run(port=54371)


def stop_gunicorn(gunicorn_process):
    """Stop Gunicorn server with a timeout."""
    gunicorn_process.terminate()  # Send SIGTERM
    try:
        gunicorn_process.wait(timeout=10)  # Wait up to 10 seconds
    except subprocess.TimeoutExpired:
        gunicorn_process.kill()


@app.route('/health/')
def health():
    return "OK"


@app.route('/callback/')
def callback():
    code = request.args.get('code')
    if code:
        # Exchange code for token (Authorization Code Grant)
        token_url = f"{config.get('aws_cognito_domain')}/oauth2/token"
        payload = {
            "grant_type": "authorization_code",
            "client_id": config.get('client_id'),
            "code": code,
            "redirect_uri": "http://localhost:54371/callback/"
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(token_url, headers=headers, data=payload)

        if response.status_code == 200:
            tokens = response.json()
            save_tokens_to_file('id_token', tokens.get('id_token'))
            save_tokens_to_file('access_token', tokens.get('access_token'))
            save_tokens_to_file('refresh_token', tokens.get('refresh_token'))
            signal_authentication_complete()
            return "Successfully logged in, return to CLI.", 200
        else:
            return jsonify(error="Failed to exchange code for tokens."), response.status_code
    else:
        return jsonify(error="No code found in the callback URL."), 400
