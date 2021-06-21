import time
import json
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver

# Untappd cookies
cookies = None

proxies = [{"ip": "79.143.87.136", "port": "9090"}, {"ip": "136.226.33.115", "port": "80"}]

# from webdriver_manager.chrome import ChromeDriverManager
# ChromeDriverManager().install()
# Path to chromedriver
driver_path = None


def get_html(url):
    url_file = urllib.request.urlopen(url)
    html = url_file.read()
    url_file.close()
    return html.decode("utf8")


def get_soup(html):
    return BeautifulSoup(html, "html.parser")


def get_abv(text):
    return float(text.split("%")[0])


def get_rating(text):
    return float(text[1:-1])


def soup_find(soup, class_):
    return soup.find(class_=class_).get_text()


def soup_find_all(soup, class_, limit=None):
    return [item.get_text() for item in soup.find_all(class_=class_, limit=limit)]


def get_cider_descrption(html, comment_size=10):
    soup = get_soup(html)
    descrption = {}
    descrption["name"] = soup.find(class_="name").h1.get_text()
    descrption["descrption"] = soup_find(soup, "beer-descrption-read-less")
    descrption["brewery"] = soup_find(soup, "brewery")
    descrption["style"] = soup_find(soup, "style")
    descrption["abv"] = get_abv(soup_find(soup, "abv"))
    descrption["rating"] = get_rating(soup_find(soup, "num"))
    descrption["comments"] = soup_find_all(soup, "comment-text", comment_size)
    return descrption


def initialize_driver(driver_path, cookies, proxy):
    options = webdriver.ChromeOptions()
    options.add_argument(f"--proxy-server=={proxy['ip']}:{proxy['port']}")
    driver = webdriver.Chrome(driver_path, options=options)
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
                driver.find_elements_by_link_text("Show More")[-1].click()
                cur_size = len(driver.find_elements_by_class_name(flag["class_name"]))
                time.sleep(5)
            except:
                continue

    html = driver.page_source
    return html


def get_dataset(url, driver_path, cookies, proxy, dataset_size=100, comment_size=40):
    driver = initialize_driver(driver_path, cookies, proxy)

    dataset_flag = {"class_name": "beer-item", "size": dataset_size}
    comment_flag = None if comment_size is None else {"class_name": "comment-text", "size": comment_size}

    html = get_html_untappd_ciders(url, driver, dataset_flag)
    soup = get_soup(html)

    cider_urls = [f"https://untappd.com{item.a['href']}" for item in soup.find_all("p", class_="name")]

    dataset = {}
    dataset_name = urllib.parse.urlparse(url)[-2][2:]
    for i, cider_url in enumerate(cider_urls[:dataset_size]):
        print(i, cider_url)
        if comment_size is None:
            cider_html = get_html(cider_url)
        else:
            cider_html = get_html_untappd_ciders(cider_url, driver, comment_flag)
        dataset[cider_url] = get_cider_descrption(cider_html, comment_size)

        time.sleep(5)

        with open(f"{dataset_name}.json", "w") as out_file:
            json.dump(dataset, out_file)

    driver.close()
    return dataset


if __name__ == "__main__":
    # можно расспараллелить по прокси
    proxy = proxies[0]
    url = "https://untappd.com/search?q=сидр"
    rus_ciders = get_dataset(url, driver_path, cookies, proxy, dataset_size=50, comment_size=20)
    with open("rus_ciders.json", "w") as out_file:
        json.dump(rus_ciders, out_file)

    proxy = proxies[1]
    url = "https://untappd.com/search?q=cider"
    foreign_ciders = get_dataset(url, driver_path, cookies, proxy, dataset_size=50, comment_size=20)
    with open("foreign_ciders.json", "w") as out_file:
        json.dump(foreign_ciders, out_file)

    all_ciders = rus_ciders.copy()
    all_ciders.update(foreign_ciders)
    with open("ciders.json", "w") as out_file:
        json.dump(all_ciders, out_file)
