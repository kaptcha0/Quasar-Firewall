import json
import os
import xml.etree.ElementTree as ET
from typing import List

from .request import Request


def get_directory(dir_name: str = ''):
    from pathlib import Path

    path_to_quasar = Path(__file__).parents[0]
    return path_to_quasar / dir_name


def parse_dataset(f: str):
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
    tree = ET.parse(f)
    root = tree.getroot()
    requests = []

    for i, sample in enumerate(root):
        class_elem = sample.find('class')
        req = sample.find('request')
        data = {}

        for item in req:
            tag = item.tag
            if tag.lower() not in ["uri", "query", "body"]:
                data[tag] = item.text

        type = class_elem.find(
            'type').text
        is_hack = False if type.lower() == 'valid' else True
        data['is_hack'] = is_hack

        requests.append(Request(data).to_dict())

    file = open("./datasets/dataset.json", "w")

    file.write(json.dumps(requests))

    file.close()
    del file
    return requests


def load_dataset(file: str = f"{get_directory('datasets') / 'web-application-attacks-datasets/ecml_pkdd/learning_dataset.xml'}"):
    """
        Handles dataset loading, returns parsed dataset in `List[Request]` form
    """
    os.chdir(str(get_directory()))

    global data
    data = None
    reqs: List[Request] = []

    if not os.path.exists("./datasets/dataset.json"):
        data = parse_dataset(file)

    try:
        with open("./datasets/dataset.json") as f:
            data = json.load(f)
            for d in data:
                reqs.append(Request(d))
    except json.decoder.JSONDecodeError as e:
        import traceback
        traceback.print_exc()

    return reqs


if __name__ == "__main__":
    load_dataset()
