
class Request(object):
    """
        Uniform `Request` object
    """

    def __init__(self, data: dict):
        self.method: str = data['method']
        self.protocol: str = data["protocol"]
        self.is_hack: bool = data['is_hack']

        try:
            self.headers = Headers(data["content_length"])
        except:
            try:
                self.headers = Headers(len(data["body"]))
            except:
                self.headers = Headers(0)

    def to_dict(self):
        """
            Returns data ins dict form
        """
        data = {
            "method": self.method,
            "protocol": self.protocol,
            "headers": self.headers.to_dict(),
            "is_hack": self.is_hack
        }
        return data


class Headers:
    """
        Uniform `Headers` object
    """

    def __init__(self, length):
        self.content_length = length if length is not None else 0

    def to_dict(self):
        data = {
            "content_length": self.content_length
        }
        return data
