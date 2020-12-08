from io import StringIO
import json
import os
import sys

from .evolution import Evolution
from .request import Request
from .request_parser import BodyParser, QueryParser


class Detector:
    def __init__(self, evolution: Evolution, body_parser: BodyParser, query_parser: QueryParser):
        self.evolution = evolution
        self.body_parser = body_parser
        self.query_parser = query_parser

    def predict(self, data, body: bytes, query: bytes):
        req = data

        if type(data) is not Request:
            data["is_hack"] = None
            req = Request(data)

        output = self.evolution.predict(req)
        self.score = output[0] * 100

        prediction = output[0] > 0.5

        body_probability = self.body_parser.predict(
            body.decode('utf-8'))[0]
        query_probabiliy = self.query_parser.predict(
            query.decode('utf-8'))[0]

        in_body = bool(round(body_probability))
        in_query = bool(round(query_probabiliy))

        return prediction or (in_body or in_query)

