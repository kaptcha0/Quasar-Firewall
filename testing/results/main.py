import csv
import json
import os
import random
import threading
from concurrent import futures

import requests

url = "http://localhost:5000"
label = "project_quasar_results"

thread_local = threading.local()
writer = csv.DictWriter(
    open(f"{label}.tsv", "w"), dialect='excel-tab', fieldnames=["Is Normal", "Actual", "Correct", "Attack Type", "Payload"], lineterminator='\n')


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def get_writer():
    if not hasattr(thread_local, "writer"):
        thread_local.writer = csv.DictWriter(
            open(f"{label}.tsv", "w"), dialect='excel-tab', fieldnames=["Is Normal", "Actual", "Correct", "Attack Type", "Payload"], lineterminator='\n')

    return writer


def process(data: dict):
    session = get_session()
    writer = get_writer()

    with session.post(url, json={"data": data["payload"]}) as res:
        prediction = res.ok
        actual = data["class"]

        d = {"Is Normal": prediction, "Actual": actual, "Correct": prediction == actual,
             "Attack Type": data["attack_type"], "Payload": f"'{data['payload']}'"}
        print(d)
        writer.writerow(d)


def send_requests(dataset: "list[dict]"):
    writer.writeheader()
    with futures.ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(process, random.sample(dataset, len(dataset)))


def extract_dataset():
    data = []

    with open("./dataset/payload_full.csv") as f:
        reader = csv.reader(f)
        labels = []

        for i, row in enumerate(reader):
            to_append = {}
            if i == 0:
                labels = row
                continue

            for j, col in enumerate(row):
                if j not in [3]:
                    to_append[labels[j]] = col
                else:
                    to_append["class"] = col.lower() == "norm"

            data.append(to_append)

    with open('./testing_dataset.json', 'w') as f:
        json.dump(data, f)

    return data


def main():
    global data

    if not os.path.exists("./testing_dataset.json"):
        data = extract_dataset()
    else:
        with open("./testing_dataset.json") as f:
            data = json.load(f)

    send_requests(data)


if __name__ == "__main__":
    main()
