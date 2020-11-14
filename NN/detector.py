from evolution import Evolution
from flask import Flask, Response
from werkzeug.wrappers import Request


class Detector(object):
    def __init__(self, app: Flask) -> None:
        self.app = app
        self.evolution: Evolution = Evolution.load('99')

    def __call__(self, environ, start_response):
        request = Request(environ, shallow=True)

        length: int = 0 if request.content_length == None else request.content_length
        output = self.evolution.predict(length)[0]

        if (output < 0.5):
            # Not a hack!
            return self.app(environ, start_response)

        #Its a hack
        res = Response(u'Hack detected',
                       mimetype='text/plain', status=404)
        return res(environ, start_response)
