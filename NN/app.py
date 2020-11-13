from flask import Flask, Response, request
import requests
from evolution import Evolution

host: str = "http://localhost:8080"

app: Flask = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return handle_get()


@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path: str):
    print(request)

    if request.method == 'GET':
        return handle_get(path)
    elif request.method == 'POST':
        return handle_post(path, request.get_json())


def init():
    print("proxy initialized")
    app.run()
    print("closing proxy")


def handle_get(path: str = ''):
    resp = requests.get(f"{host}/{path}")
    excluded_headers = ['content-encoding',
                        'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items(
    ) if name.lower() not in excluded_headers]
    response = Response(resp.content, resp.status_code, headers)
    return response


def handle_post(path: str = '', body: dict = {}):
    resp = requests.post(f"{host}/{path}", json=body)
    excluded_headers = ["content-encoding", "content-length", "transfer-encoding", "connection"]
    headers = [(name, value) for (name, value) in resp.raw.headers.items(
    ) if name.lower() not in excluded_headers]
    response = Response(resp.content, resp.status_code, headers)
    return response
