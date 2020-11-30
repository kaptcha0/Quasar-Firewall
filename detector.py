import os

from flask import Flask, Response
from werkzeug.wrappers import Request

import request as r
from evolution import Evolution
from request_parser import BodyParser, QueryParser

class Detector(object):
    """
        Middleware for detecting hacks
    """

    def __init__(self, app: Flask):
        self.app = app
        self.evolution: Evolution = Evolution.load('199', './session-1')
        self.body_parser = BodyParser.load().model
        self.query_parser = QueryParser.load().model
        
        try:
            os.system('cls')
        except:
            os.system('clear')

    def __call__(self, environ, start_response):
        """
            Called by middleware. Actually does the detecting.
        """
        
        request = Request(environ)

        data = r.Request({
            "method": request.method,
            "headers": str(request.headers),
            "protocol": request.environ.get('SERVER_PROTOCOL'),
            "is_hack": None
        })

        output = self.evolution.predict(data)
        self.score = [output[1] * 100, output[0] * 100]

        prediction = output[0] > output[1]

        body_probability = self.body_parser.predict(request.data.decode('utf-8'))
        query_probabiliy = self.query_parser.predict(request.query_string.decode('utf-8'))
        
        if prediction:
            # Not a hack!
            res = Response(u'Not Hack {0} % sure {1} % not sure\n Request {2}\nRaw Score: {3}'.format(self.score[1], self.score[0], data.to_dict(), output),
                           mimetype='text/plain', status=200)
            return res(environ, start_response)
        
        # Its a hack
        res = Response(u'Hack detected {0} % sure {1} % not sure\n Request {2}\nRaw Score: {3}'.format(self.score[0], self.score[1], data.to_dict(), output),
                       mimetype='text/plain', status=404)
        return res(environ, start_response)



