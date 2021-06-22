import json
import requests


def get_params(text):
    return {"q": text, "langpair": "en|ru", "de": "a@b.c", "onlyprivate": "0", "mt": "1"}


def translate(text):
    headers = {
        "x-rapidapi-key": None,
        "x-rapidapi-host": "translated-mymemory---translation-memory.p.rapidapi.com",
    }

    querystring = get_params(text)
    url = "https://translated-mymemory---translation-memory.p.rapidapi.com/api/get"
    response = requests.get(url, headers=headers, params=querystring)
    return json.loads(response.text)["responseData"]["translatedText"]


if __name__ == "__main__":
    with open("foreign_ciders.json") as input_file:
        cider_data = json.load(input_file)

    for cider in list(cider_data.values()):
        cider["descrption"] = translate(cider["descrption"])
        translate_comments = []
        for comment in cider["comments"]:
            translate_comments.append(translate(comment))
        cider["comments"] = translate_comments

    with open("translate_foreign_ciders.json", "w") as out_file:
        json.dump(cider_data, out_file)
