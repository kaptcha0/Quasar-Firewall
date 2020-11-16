import re


class Request:
    def __init__(self, data: dict):
        self.method: str = data['method']
        self.protocol: str = data["protocol"]
        self.is_hack: bool = data['is_hack']
        self.headers: Headers = Headers(data['headers'])

    def to_json(self):
        data = {
            "method": self.method,
            "protocol": self.protocol,
            "headers": self.headers.to_json(),
            "is_hack": self.is_hack
        }
        return data


class Headers:
    def __init__(self, data):
        self.content_length = 0
        if type(data) is str:
            # Find end of Content-Length tag
            num_of_digits = 5
            search = 'Content-Length: '
            index = data.find(search)
            if index == -1:
                return

            digits = data[index:num_of_digits]
            # print(test_str)

            # Find consecutive numbers
            d = re.findall(r'\d+', digits)
            try:
                self.content_length = d[0]
            except:
                self.content_length = 0
        elif type(data) is dict:
            self.content_length = data["content_length"]
        else:
            print(f'type {type(data)} is not supported')

    def to_json(self):
        data = {
            "content_length": self.content_length
        }
        return data
