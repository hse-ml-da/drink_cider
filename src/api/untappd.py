import time
import json
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver

cookies = {
    '__utma': '13579763.1930691142.1623785772.1623922407.1623926840.4', # меняется
    '__utmb': '13579763.24.9.1623931091022', # меняется
    '__utmc': '13579763',
    '__utmz': '13579763.1623926840.4.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
    '__utmt': '1',
    '_ALGOLIA': '99142a65-8111-4d7b-b788-c4565716d5b9',
    'untappd_user_v3_e' : 'c2f3a8cf34aaba61afda364ea7cc98a0f0731afbf43c3bfe2e3243b4d9a12216bf5ab645d478a5e9076f16b2b27f7637ab5c88b3304d57af7fad02f97d1a597d3ZfUjmK1oQDtcoWl%2B9%2FyLjfSNmrAekHnLqLTU23ATpKfeB808Lprbql%2BMYx3KLjg9OdH%2FozbguIKPMz1IbYetA%3D%3D',
    'ut_d_l': '7ca0d74e18218e26345aa5be52298c12fcfc0d3a7783b9d89ccce2df3422f0cad77bc7646f7a15fb212c5ff261caf8e87b2a39afc6a894f4ad479f432bf4661cVLeFP0RVh88qm7okaUgG8izqeSUrCToPO4px0cza4CBhK39VH30TXnvkonXXn6tBAaP9lQkYSCj6WpTJgSN2ow%3D%3D',
    '__gads': 'ID=0cb79354f00e9e22-227c9c5062c800d7:T=1623785784:RT=1623785784:S=ALNI_MbkTFO32OJY9qGxz6FtSvNGFO2_Qg',
    'FCCDCF': "[['AKsRol8D1vSInhHSM4yX31mseEJAfgFs-LRHMAJLhR8HJZC73NWOR6zAyB-3T6M7kjynhdJHFwC7CBgeokFuXTU1C-gwlD-_B8JxvXHVr93_Y3Ma4_m0w2e49IszhizY-CnW2qNfj8OaIi0kLJTYSON13HohrFsffQ=='],null,['[[],[],[],[],null,null,true]',1623785772516],null]",
    '_ga': 'GA1.2.1930691142.1623785772',
    'sliguid': '64c7a56e-6466-459a-a591-a7809684ab93',
    'slireg': 'https://scout.us2.salesloft.com',
    'slirequested': 'true'
}


def get_html(url):
    url_file = urllib.request.urlopen(url)
    html = url_file.read()
    url_file.close()
    return html.decode("utf8")


def get_soup(html):
    return BeautifulSoup(html, "html.parser")


def soup_find(soup, class_):
    return soup.find(class_=class_).get_text()


def soup_find_all(soup, class_, limit=None):
    return [item.get_text() for item in soup.find_all(class_=class_, limit=limit)]


def get_cider_description(html, comment_size=10):
    soup = get_soup(html)
    description = {}
    description["name"] = soup.find(class_="name").h1.get_text()
    description["description"] = soup_find(soup, "beer-descrption-read-less")
    description["brewery"] = soup_find(soup, "brewery")
    description["abv"] = soup_find(soup, "abv")
    description["rating"] = soup_find(soup, "num")
    description["style"] = soup_find(soup, "style")
    description["comments"] = soup_find_all(soup, "comment-text", comment_size)
    return description


def initialize_driver(cookies):
    driver = webdriver.Safari()
    driver.get("https://untappd.com")

    for name, value in cookies.items():
        driver.add_cookie({"name": name, "value": value})

    return driver


def get_html_untappd_ciders(url, driver, flag=None):
    driver.get(url)

    if flag is not None:
        cur_size = len(driver.find_elements_by_class_name(flag["class_name"]))
        while cur_size <= flag["size"]:
            try:
                driver.find_elements_by_link_text('Show More')[-1].click()
                cur_size = len(driver.find_elements_by_class_name(flag["class_name"]))
                time.sleep(5)
            except:
                continue

    html = driver.page_source
    return html


def get_dataset(url, cookies, dataset_size=100, comment_size=40):
    driver = initialize_driver(cookies)

    dataset_flag = {"class_name": "beer-item", "size": dataset_size}
    comment_flag = None if comment_size is None else {"class_name": "comment-text", "size": comment_size}

    html = get_html_untappd_ciders(url, driver, dataset_flag)
    soup = get_soup(html)

    cider_urls = [f"https://untappd.com{item.a['href']}" for item in soup.find_all("p", class_="name")]

    dataset = {}
    for i, cider_url in enumerate(cider_urls[:dataset_size]):
        print(i, cider_url)
        if comment_size is None:
            cider_html = get_html(cider_url)
        else:
            cider_html = get_html_untappd_ciders(cider_url, driver, comment_flag)

        dataset[cider_url] = get_cider_description(cider_html, comment_size)
        time.sleep(5)

    driver.close()
    return dataset


if __name__ == "__main__":
    url = "https://untappd.com/search?q=сидр"
    rus_ciders = get_dataset(url, cookies, dataset_size=50, comment_size=20)

    url = "https://untappd.com/search?q=cider"
    foreign_ciders = get_dataset(url, cookies, dataset_size=50, comment_size=20)

    all_ciders = rus_ciders.copy()
    all_ciders.update(foreign_ciders)
    with open("ciders.json", "w") as out_file:
        json.dump(all_ciders, out_file)
