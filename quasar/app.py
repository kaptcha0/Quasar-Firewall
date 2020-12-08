import requests
from flask import Flask, Response, request

from .detector_flask import DetectorMiddleware

host: str = "http://localhost:8080"

app: Flask = Flask(__name__)
app.wsgi_app = DetectorMiddleware(app.wsgi_app)


@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'PATCH', 'delete'.upper()])
def proxy(path:str):
    print(request)

    if request.method == 'GET':
        return handle_get(path)
    elif request.method == 'POST':
        return handle_post(path, request.get_json())
    elif request.method == 'PUT':
        return handle_put(path, request.get_json())
    elif request.method == 'PATCH':
        return handle_patch(path, request.get_json())
    elif request.method == 'delete'.upper():
        return handle_delete(path, request.get_json())


def init(debug: bool = False, port: int = 5000, proxy_target: str = "http://localhost:8080"):
    global host
    app.run(debug=debug, port=port)
    host = proxy_target


def handle_get(path: str = ''):
    resp = requests.get(f"{host}/{path}")
    headers = [(name, value) for (name, value) in resp.raw.headers.items()]
    response = Response(resp.content, resp.status_code, headers)
    return response


def handle_post(path: str = '', body: dict = {}):
    resp = requests.post(f"{host}/{path}", json=body)
    headers = [(name, value) for (name, value) in resp.raw.headers.items()]
    response = Response(resp.content, resp.status_code, headers)
    return response


def handle_patch(path: str = '', body: dict = {}):
    resp = requests.patch(f"{host}/{path}", json=body)
    headers = [(name, value) for (name, value) in resp.raw.headers.items()]
    response = Response(resp.content, resp.status_code, headers)
    return response


def handle_put(path: str = '', body: dict = {}):
    resp = requests.put(f"{host}/{path}", json=body)
    headers = [(name, value) for (name, value) in resp.raw.headers.items()]
    response = Response(resp.content, resp.status_code, headers)
    return response


def handle_delete(path: str = '', body: dict = {}):
    resp = requests.delete(f"{host}/{path}", json=body)
    headers = [(name, value) for (name, value) in resp.raw.headers.items()]
    response = Response(resp.content, resp.status_code, headers)
    return response
