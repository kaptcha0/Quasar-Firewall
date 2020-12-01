import csv
import json
import os

import requests

methods = ["sqli", "xss", "cmdi", "path-traversal"]


def send_requests(dataset: "list[dict]", url: str, label: str):
    with open("results.csv", "w") as f:
        writer = csv.DictWriter(
            f, fieldnames=["Prediction", "Actual", "Correct", "Attack Type", "Label"])
        writer.writeheader()

        for item in dataset:
            res = requests.post(url, item["payload"])
            prediction = res.ok
            actual = item["class"]

            d = {"Prediction": prediction, "Actual": actual, "Correct": prediction == actual,
                 "Attack Type": item["attack_type"], "Label": label}
            print(d)
            writer.writerow(d)


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

    send_requests(data, "http://localhost:5000", "My Firewall")


if __name__ == "__main__":
    main()
