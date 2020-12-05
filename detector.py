from io import StringIO
import json
import os
import sys

from evolution import Evolution
from request import Request
from request_parser import BodyParser, QueryParser


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

if __name__ == "__main__":
    data = json.loads(sys.argv[1])
    body = str(sys.argv[2]).encode('utf-8')
    query = str(sys.argv[3]).encode('utf-8')
    output = sys.stdout
    os.chdir("../")
    sys.stdout = StringIO()

    detector = Detector(Evolution.load("99", "checkpoints"),
                        BodyParser.load(), QueryParser.load())

    valid = detector.predict(data, body, query)

    sys.stdout = output

    result = {"valid": bool(valid)}
    print(json.dumps(result))

    sys.stdout.flush()
