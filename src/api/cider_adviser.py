import json
import pickle
import re
from dataclasses import dataclass
from logging import getLogger
from os import environ
from os.path import join, exists
from urllib.request import URLopener

import nltk
import numpy as np
from nltk.corpus import stopwords
from pymystem3 import Mystem
from stop_words import get_stop_words


@dataclass
class CiderDescription:
    url: str
    name: str
    brewery: float
    style: str
    abv: float
    rating: float
    comments: list


class CiderAdviser:
    __vectorized_cider_url_env = "VECTORIZED_CIDER_URL"
    __vectorized_cider_descriptions = join("src", "resources", "ciders_with_tf_idf.json")
    __vectorization_model_path = join("src", "resources", "vectorizer.pickle")
    __enabled = True

    def __init__(self):
        self.__logger = getLogger(__file__)

        if not exists(self.__vectorized_cider_descriptions):
            self.__logger.info(f"Can't find cider descriptions: {self.__vectorized_cider_descriptions}")
            url = environ.get(self.__vectorized_cider_url_env)
            if url is None:
                self.__logger.error(f"No url in {self.__vectorized_cider_url_env} thus disable module")
                self.__enabled = False
                return
            url_opener = URLopener()
            url_opener.retrieve(url, self.__vectorized_cider_descriptions)

        with open(self.__vectorized_cider_descriptions) as input_file:
            self.__cider_data = json.load(input_file)
        self.__tf_idf = np.array([cider["tf_idf"] for cider in self.__cider_data.values()])

        with open(self.__vectorization_model_path, "rb") as input_file:
            self.__vectorizer = pickle.load(input_file)

        nltk.download("stopwords")
        self.__russian_stopwords = get_stop_words("ru")
        self.__russian_stopwords.extend(stopwords.words("russian"))
        self.__mystem = Mystem()

    @property
    def enabled(self) -> bool:
        return self.__enabled

    def __parse(self, message: str) -> str:
        re_message = re.sub(r"[A-z!.,?:()%\'/\n\d+—-]", "", message.lower())
        tokens = self.__mystem.lemmatize(re_message)
        tokens = [
            token for token in tokens if token != " " and len(token) > 2 and token not in self.__russian_stopwords
        ]

        return " ".join(tokens)

    def get_advise(self, message: str) -> CiderDescription:
        parse_message = self.__parse(message)
        vectorized_message = self.__vectorizer.transform([parse_message]).toarray()
        res_index = self.__tf_idf.dot(vectorized_message.T).argmax()
        res_key = list(self.__cider_data.keys())[res_index]
        res_cider = self.__cider_data[res_key]
        return CiderDescription(
            res_key,
            res_cider["name"],
            res_cider["brewery"],
            res_cider["style"],
            res_cider["abv"],
            res_cider["rating"],
            res_cider["comments"],
        )
