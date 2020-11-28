from flask import Flask, Response
from werkzeug.wrappers import Request

import request as r
from evolution import Evolution


class Detector(object):
    """
        Middleware for detecting hacks
    """

    def __init__(self, app: Flask):
        self.app = app
        self.evolution: Evolution = Evolution.load('99')

    def __call__(self, environ, start_response):
        """
            Called by middleware. Actually does the detecting.
        """

        request = Request(environ)

        data = r.Request({
            "method": request.method,
            "headers": str(request.headers),
            "protocol": request.environ.get('SERVER_PROTOCOL'),
            "body": request.data.decode('utf-8'),
            "query": request.query_string.decode(),
            "is_hack": None
        })

        output = self.evolution.predict(data)
        #   0: Is a hack        1: Is not a hack
        self.score = [output[1] * 100, output[0] * 100]

        prediction = (output[0] > output[1]) and (output[0] > 0.85)

        if prediction:
            # Not a hack!
            res = Response(u'Not Hack {0} % sure {1} % not sure'.format(self.score[1], self.score[0]),
                           mimetype='text/plain', status=404)
            return res(environ, start_response)
        
        # Its a hack
        res = Response(u'Hack detected {0} % sure {1} % not sure\n Request {2}'.format(self.score[0], self.score[1], data.to_dict()),
                       mimetype='text/plain', status=404)
        return res(environ, start_response)

