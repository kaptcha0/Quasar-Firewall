from typing import List
from request import Request
import xml.etree.ElementTree as ET
import os
import json


def parse_dataset(file:str):
    """
        - Parses the dataset
        - Input dataset must be xml
            * Class - Valid request or not
            * Request
                - Method - `method`
                - Protocol - `protocol`
                - Headers - `headers`
                    * `Content-Length` and `Body` are important, but optional
        - Returns requests in `List[dict]` form
        - Creates `dataset.json` file
    """
    tree = ET.parse(file)
    root = tree.getroot()
    requests = []

    for sample in root:
        class_elem = sample.find('class')
        request = sample.find('request')
        data = {}

        for item in request:
            tag = item.tag
            if tag.lower() not in ["query", "uri"]:
                data[tag] = item.text

        type: str = class_elem.find(
            'type').text
        is_hack = False if type.lower() == 'valid' else True
        data['is_hack'] = is_hack

        requests.append(Request(data).to_json())

    file = open("dataset.json", "w")

    file.write(json.dumps(requests))

    file.close()
    del file
    return requests


def load_dataset(file:str="C:/Users/JCKab/OneDrive/Desktop/Firewall/NN/web-application-attacks-datasets/ecml_pkdd/learning_dataset.xml"):
    """
        Handles dataset loading, returns parsed dataset in `List[Request]` form
    """

    global data
    data = None
    reqs: List[Request] = []

    if not os.path.exists("./dataset.json"):
        data = parse_dataset(file)

    try:
        with open("./dataset.json") as f:
            data = json.load(f)
            for d in data:
                reqs.append(Request(d))
    except json.decoder.JSONDecodeError:
        os.remove('./dataset.json')
        raise Exception("An error occured, please try again later")

    return reqs


if __name__ == "__main__":
    load_dataset()
