import re
import pickle

import nltk
from pymystem3 import Mystem
from stop_words import get_stop_words
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer


class TFIDFParser:
    def __init__(self):
        nltk.download("stopwords")
        self.__russian_stopwords = get_stop_words("ru")
        self.__russian_stopwords.extend(stopwords.words("russian"))
        self.__mystem = Mystem()

    def __call__(self, message: str) -> str:
        re_message = re.sub(r"[A-z!.,?:()%\'/\n\d+—-]", r" ", message.lower())
        tokens = self.__mystem.lemmatize(re_message)
        tokens = [
            token for token in tokens if token != " " and len(token) > 2 and token not in self.__russian_stopwords
        ]

        return " ".join(tokens)


if __name__ == "__main__":
    with open("ciders.pickle", "rb") as input_file:
        cider_data = pickle.load(input_file)

    parser = TFIDFParser()
    cider_documents = []
    for cider in cider_data.values():
        filtering_comment = list(map(lambda comment: comment if len(comment.split()) > 2 else "", cider["comments"]))
        global_comment = ". ".join(filtering_comment)
        cider_document = " ".join([cider["descrption"], global_comment])
        cider_lema_document = " ".join([cider["name"], cider["brewery"], cider["style"], parser(cider_document)])
        cider_documents.append(cider_lema_document)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(cider_documents)
    for i, cider in enumerate(list(cider_data.values())):
        cider["tf_idf"] = X[i]

    with open("vectorizer.pickle", "wb") as output_file:
        pickle.dump(vectorizer, output_file)

    with open("ciders_with_tf_idf.pickle", "wb") as output_file:
        pickle.dump(cider_data, output_file)
