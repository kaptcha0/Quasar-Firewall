from evolution import Evolution
from flask import Flask, Response
from werkzeug.wrappers import Request
import request as r


class Detector(object):
    def __init__(self, app: Flask) -> None:
        self.app = app
        self.evolution: Evolution = Evolution.load('99')

    def __call__(self, environ, start_response):
        request = Request(environ, shallow=True)
        
        data = r.Request({
            "method": request.method,
            "headers": str(request.headers),
            "protocol": request.environ.get('SERVER_PROTOCOL'),
            "is_hack": None
        })

        output = self.evolution.predict(data)

        if (output[1] < output[0]):
            # Not a hack!
            return self.app(environ, start_response)

        #Its a hack
        res = Response(u'Hack detected',
                       mimetype='text/plain', status=404)
        return res(environ, start_response)
