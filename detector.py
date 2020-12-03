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
        self.evolution: Evolution = Evolution.load('499', './checkpoints')
        self.body_parser = BodyParser.load()
        self.query_parser = QueryParser.load()

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
            "content_length": request.content_length,
            "protocol": request.environ.get('SERVER_PROTOCOL'),
            "is_hack": None
        })

        output = self.evolution.predict(data)
        self.score = output[0] * 100

        prediction = output[0] > 0.5

        body_probability = self.body_parser.predict(
            request.get_data().decode('utf-8'))[0]
        query_probabiliy = self.query_parser.predict(
            request.query_string.decode('utf-8'))[0]

        hack_in_body = bool(round(body_probability))
        hack_in_query = bool(round(query_probabiliy))

        if prediction or (hack_in_body or hack_in_query):
                # Its a hack
                res = Response(u'Hack detected {0} % sure \nRequest {1}\nRaw Score: {2}\n\nIs hack in query string: {3}\nIs hack in body: {4}'.format(abs(self.score), data.to_dict(), output, query_probabiliy, body_probability),
                            mimetype='text/plain', status=404)
                return res(environ, start_response)

        # Not a hack!
        res = Response(u'Not Hack {0} % sure \nRequest {1}\nRaw Score: {2}\n\nIs hack in query string: {3}\nIs hack in body: {4}'.format(self.score, data.to_dict(), output, query_probabiliy, body_probability),
                       mimetype='text/plain', status=200)
        return res(environ, start_response)
