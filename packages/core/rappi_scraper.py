import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


class RappiParser:

    def get_categories(self):
        page = requests.get("{}/restaurantes".format(self.main_url))
        soup = BeautifulSoup(page.content, "html.parser")
        categories = {}

        job_elements = soup.find_all("span", attrs={"data-testid": "typography",
                                                    "class": "sc-bxivhb eeSaHG sc-5d042f5c-5 gzdxii"})
        for i, job_element in enumerate(job_elements):
            elements = job_element.text
            categories[elements] = i + 1

        return categories

    def __init__(self, main_url="https://www.rappi.cl"):
        self.main_url = main_url
        self.categories = self.get_categories()

    def get_restaurants_urls(self, category):
        driver = webdriver.Chrome()
        driver.get("{}/restaurantes".format(self.main_url))
        restaurants_urls = []
        id_cat = self.categories[category]
        xpath = '//*[@id="__next"]/div[3]/div[3]/div[1]/div/div/button[{}]'.format(
            id_cat)

        driver.find_element(By.XPATH, xpath).click()
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        job_elements = soup.find_all("a", attrs={"data-testid": "store-item"})

        for job_element in job_elements:
            restaurants_urls.append(job_element["href"])

        driver.close()

        return restaurants_urls

    def get_restaurants_results(self, restaurants_urls, limit=1000):
        restaurants_results = pd.DataFrame()

        for i, url in enumerate(restaurants_urls):

            if i > limit:
                break

            new_url = "{}{}".format(self.main_url, url)
            page = requests.get(new_url)
            soup = BeautifulSoup(page.content, "html.parser")

            print("({}/{}) parsing:".format(i+1, len(restaurants_urls)), new_url)

            name = soup.find("h1", {"class": "chakra-text css-6oec1p"}).text
            address = soup.find("h2", {"class": "sc-bxivhb dVvqfA"}).text
            stars = soup.find("span", {"class": "sc-bxivhb fyzoZN"}).text

            try:
                stars = float(stars)
            except ValueError:
                stars = None

            all_products = soup.find_all("div", {
                "class": "sc-5a7def68-0 hbVrBp sc-a04fe063-1 hQgbBh"})

            obs = {"link": new_url,
                   "name": name,
                   "address": address,
                   "stars": stars,
                   "total_products": len(all_products)}
            restaurants_results = restaurants_results.append(obs, ignore_index=True)

        print("Total results:", len(restaurants_results))
        return restaurants_results
