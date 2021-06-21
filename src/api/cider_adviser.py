import os
import re
import json
import pickle
import numpy as np
from pymystem3 import Mystem
from stop_words import get_stop_words
from nltk.corpus import stopwords


class CiderAdviser:
    def __init__(self):
        self.__russian_stopwords = get_stop_words('ru')
        self.__russian_stopwords.extend(stopwords.words('russian'))
        self.__mystem = Mystem()

        with open(os.path.join("src", "resources", "ciders_with_tf_idf.json")) as input_file:
            self.__cider_data = json.load(input_file)
        self.__tf_idf = np.array([cider['tf_idf'] for cider in self.__cider_data.values()])

        with open(os.path.join("src", "resources", "vectorizer.pickle", "rb")) as input_file:
            self.__vectorizer = pickle.load(input_file)

    def __parse(self, message: str) -> str:
        re_message = re.sub(r'[A-z!.,?:()%\'/\n\d+—-]', '', message.lower())
        tokens = self.__mystem.lemmatize(re_message)
        tokens = [token for token in tokens
                  if token != " " and len(token) > 2 and token not in self.__russian_stopwords]

        return " ".join(tokens)

    def get_advise(self, message: str) -> str:
        parse_message = self.__parse(message)
        vectorize_message = self.__vectorizer.transform([parse_message]).toarray()
        res_index = self.__tf_idf.dot(vectorize_message.T).argmax()
        res_key = list(self.__cider_data.keys())[res_index]
        return f"name : {self.__cider_data[res_key]['name']}, \nurl: {res_key}"
