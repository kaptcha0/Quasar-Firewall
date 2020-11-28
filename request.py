import sys
from math import sqrt

class Request(object):
    """
        Uniform `Request` object
    """

    def __init__(self, data: dict):
        self.method: str = data['method']
        self.protocol: str = data["protocol"]
        self.is_hack: bool = data['is_hack']

        try:
            self.headers = Headers(len(data["body"]))
        except:
            self.headers = Headers(0)

        self.body = self.__encode__(data["body"])
        self.query = self.__encode__(data["query"])
    
    def __encode__(self, data: str):
        data = str(data) if data != None else '\0'
        num = "".join([str(ord(i)) for i in data])

        try:
            normalized = sqrt(
                (int(num) % int(sys.float_info.max))) / sys.maxsize
            return float(normalized)
        except TypeError:
            return 0.0
        except ValueError:
            return 0.0
        
    def to_dict(self):
        """
            Returns data ins dict form
        """
        data = {
            "method": self.method,
            "protocol": self.protocol,
            "headers": self.headers.to_dict(),
            "is_hack": self.is_hack,
            "query": self.query,
            "body": self.body
        }
        return data


class Headers:
    """
        Uniform `Headers` object
    """

    def __init__(self, length):
        self.content_length = length

    def to_dict(self):
        data = {
            "content_length": self.content_length
        }
        return data
