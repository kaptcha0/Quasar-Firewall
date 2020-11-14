import xml.etree.ElementTree as ET


def load_dataset():
    file = "C:/Users/JCKab/OneDrive/Desktop/Firewall/NN/web-application-attacks-datasets/ecml_pkdd/learning_dataset.xml"
    tree = ET.parse(file)
    root = tree.getroot()
    requests = []
    # print(root.iter('sample'))

    for sample in root:
        request = sample.find('{http://www.example.org/ECMLPKDD}request')
        _request = []

        for item in request:
            data = {}
            tag = item.tag[33:]
            data[tag] = item.text
            _request.append(data)
        
        requests.append(_request)
    
    file = open("dataset.json", "w")

    file.write(str(requests))

    file.close()
    del file
    return requests


if __name__ == "__main__":
    load_dataset()
