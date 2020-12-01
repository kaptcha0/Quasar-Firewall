import json
import os
import xml.etree.ElementTree as ET
from typing import List

import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression


class BodyParser(object):
    def __init__(self, model: LogisticRegression = None, word_list: str = "./words.json"):
        with open(word_list) as f:
            data: dict = json.load(f)

        vectorizer = CountVectorizer(min_df=0, lowercase=True)
        vectorizer.fit(data.keys())
        self.formated = vectorizer.vocabulary_
        self.vectorizer = vectorizer
        self.model = model

    def train(self, save_model: bool = False, filename: str = './body_model.sav'):
        raw_data = self.__load_dataset__()

        training_data = []
        training_labels = []

        for x in raw_data:
            training_data.append(str(x[0]))

            training_labels.append(int(x[1]))

        vectorized_data = self.vectorizer.transform(training_data)

        classifier = LogisticRegression(max_iter=50000) if self.model == None else self.model
        classifier.fit(vectorized_data, training_labels)
        if save_model is True:
            joblib.dump(classifier, filename)

        return classifier

    def predict(self, input: str):
        v_input = self.vectorizer.transform([input])
        return self.model.predict(v_input)

    @staticmethod
    def load(filename: str = "./body_model.sav"):
        if not filename.endswith('.sav'):
            filename = filename + '.sav'

        model = joblib.load(filename)
        return BodyParser(model)

    def __load_dataset__(self, file: str = "./web-application-attacks-datasets/ecml_pkdd/learning_dataset.xml"):
        """
            Handles dataset loading, returns parsed dataset in `List[List[str]]` form
        """

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
                - Creates `dataset_s.json` file
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
                    if tag.lower() in ["query", "body"]:
                        data[tag] = item.text

                if req.find('body') == None:
                    data["body"] = '\0'

                if "query" not in data.keys():
                    data["query"] = '\0'

                type = class_elem.find('type').text
                is_hack = False if type.lower() == 'valid' else True
                data['is_hack'] = is_hack

                requests.append(data)

            file = open("dataset_s.json", "w")
            file.write(json.dumps(requests))
            file.close()
            del file

            return requests

        global data
        data = None
        dataset: List[List[str]] = []

        if not os.path.exists("./dataset_s.json"):
            data = parse_dataset(file)

        try:
            if data is None:
                with open("./dataset_s.json") as f:
                    data = json.load(f)

            for d in data:
                dataset.append([d["body"], d["is_hack"]])
        except json.decoder.JSONDecodeError:
            os.remove('./dataset_s.json')
            raise RuntimeError("An error occured, please try again later")

        return dataset


class QueryParser(BodyParser):
    def __init__(self, model: LogisticRegression = None, word_list: str = "./words.json"):
        super().__init__(model, word_list)

    def __load_dataset__(self, file: str = "./web-application-attacks-datasets/ecml_pkdd/learning_dataset.xml"):
        """
            Handles dataset loading, returns parsed dataset in `List[List[str]]` form
        """

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
                - Creates `dataset_s.json` file
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
                    if tag.lower() in ["query", "body"]:
                        data[tag] = item.text

                if req.find('body') == None:
                    data["body"] = '\0'

                if "query" not in data.keys():
                    data["query"] = '\0'

                type = class_elem.find('type').text
                is_hack = False if type.lower() == 'valid' else True
                data['is_hack'] = is_hack

                requests.append(data)

            file = open("dataset_s.json", "w")
            file.write(json.dumps(requests))
            file.close()
            del file

            return requests

        global data
        data = None
        dataset: List[List[str]] = []

        if not os.path.exists("./dataset_s.json"):
            data = parse_dataset(file)

        try:
            if data is None:
                with open("./dataset_s.json") as f:
                    data = json.load(f)

            for d in data:
                dataset.append([d["query"], d["is_hack"]])
        except json.decoder.JSONDecodeError:
            os.remove('./dataset_s.json')
            raise RuntimeError("An error occured, please try again later")

        return dataset

    def train(self, save_model: bool = False, filename: str = './query_model.sav'):
        raw_data = self.__load_dataset__()

        training_data = []
        training_labels = []

        for x in raw_data:
            training_data.append(str(x[0]))

            training_labels.append(int(x[1]))

        vectorized_data = self.vectorizer.transform(training_data)

        classifier = LogisticRegression(
            max_iter=50000) if self.model == None else self.model
        classifier.fit(vectorized_data, training_labels)
        if save_model is True:
            joblib.dump(classifier, filename)

        return classifier

    @staticmethod
    def load(filename: str = "./query_model.sav"):
        if not filename.endswith('.sav'):
            filename = filename + '.sav'

        model = joblib.load(filename)
        return QueryParser(model)
