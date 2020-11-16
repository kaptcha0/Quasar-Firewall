from request import Request
import xml.etree.ElementTree as ET
import os
import json


def parse_dataset():
    file = "C:/Users/JCKab/OneDrive/Desktop/Firewall/NN/web-application-attacks-datasets/ecml_pkdd/learning_dataset.xml"
    tree = ET.parse(file)
    root = tree.getroot()
    requests = []

    for sample in root:
        class_elem = sample.find('{http://www.example.org/ECMLPKDD}class')
        request = sample.find('{http://www.example.org/ECMLPKDD}request')
        data = {}

        for item in request:
            tag = item.tag[33:]
            if tag.lower() not in ["query", "uri"]:
                data[tag] = item.text

        type: str = class_elem.find(
            '{http://www.example.org/ECMLPKDD}type').text
        is_hack = False if type.lower() == 'valid' else True
        data['is_hack'] = is_hack

        requests.append(Request(data).to_json())

    file = open("dataset.json", "w")

    file.write(json.dumps(requests))

    file.close()
    del file
    return requests


def load_dataset():
    global data
    data = None
    reqs = []

    if not os.path.exists("./dataset.json"):
        data = parse_dataset()

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
