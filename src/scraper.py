import selenium
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
import bs4
from bs4 import  BeautifulSoup
import requests
import lxml
import re


import concurrent.futures
from typing import List, Dict

class Scraper:

    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    APARTMENT_DETAILS = [
        "Gross Area",
        "Interior Area",
        "Bedrooms",
        "Baths",
        "Floor",
        "Type",
        "Status",
        "Price",
        "City"
    ]



    def __init__(self):
        self.options = Options()
        self.options.page_load_strategy = 'normal'
        self.driver = webdriver.Chrome(options = self.options)


    def load_webpage(self, url: str)-> None:
        self.driver.get(url)

    def scrape_links_from_page(self):
        # Find the divs with the specified classes
        properties_div = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'card card-list')]")

        # List to store the links
        links = []

        # Iterate through each div in the list
        for div in properties_div:
            # Find the 'a' elements within each div
            links_within_div = div.find_elements(By.TAG_NAME, 'a')

            # Iterate through each 'a' element within the div
            for link in links_within_div:
                # Get the URL of the link
                link_url = link.get_attribute("href")

                # Add the link URL to the list
                links.append(link_url)

        return links

    def scrape_all_links(self)-> List[str]:

        all_links = []
        num_web_pages_to_scrape = 531

        for _ in range(num_web_pages_to_scrape - 1):
            try:
                # Find and click the "next" button
                next_button = self.driver.find_element(By.XPATH, "//li[contains(@class, 'page-item')]")
                next_button.click()

                # Add a waiting period to allow the next page to load
                self.driver.implicitly_wait(5)  # Adjust as needed

                # Scrape links from the current page
                current_links = self.scrape_links_from_page()

                # Extend the list of all_links with the current_links
                all_links.extend(current_links)

            except NoSuchElementException:
                # Break the loop if there is no "next" button found
                break

        # Close the browser window
        self.driver.close()

        # Return the final list of links
        return all_links

    def format_links(self)-> List[str]:

        resulting_links = self.scrape_all_links()
        return [link for link in resulting_links if link != '']

    def process_url(self, url):
        try:
            r = requests.get(url, headers= Scraper.HEADERS)
            r.raise_for_status()  # Raise an HTTPError for bad responses
            page_html = BeautifulSoup(r.text, 'lxml')
            apartment_paragraphs = page_html.find_all('div', class_="card-body col-md-12")
            price = page_html.find_all('div', class_="col-lg-4 col-md-4 text-right")
            location = page_html.find_all('div', class_="col-lg-12 col-md-12")


            return url, apartment_paragraphs, price, location
        except Exception as e:
            return url, None, None, None

    def return_all(self):
        all_paragraphs = []
        all_headings = []
        all_locations = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # Use executor.map to apply the process_url function to each URL concurrently
            results = executor.map(self.process_url, self.format_links())

        for url, paragraphs, price, location in results:
            if paragraphs is not None and price is not None:
                all_paragraphs.append(paragraphs)
                all_headings.append(price)
                all_locations.append(location)
            else:
                continue

        return all_paragraphs, all_headings, all_locations


    def extract_apartment_details(self, apartment: List[str], details: List[str])->Dict[str, List[str]]:

        result_dict_apartment_details = {}

        for col_name in apartment:
            pattern = re.compile(fr'{col_name}:\n(.+?)\n')
            col_values = [pattern.search(detail).group(1) for detail in details if pattern.search(detail)]
            result_dict_apartment_details[col_name] = col_values

        return result_dict_apartment_details

    def extract_price(self, prices: List[str], details: List[str])->Dict[str, List[str]]:

        result_dict_price_details = {}

        for price in prices:

            result_dict_price_details[price] = details

        return result_dict_price_details

    def extract_city(self, cities: List[str],details: List[str])-> Dict[str, List[str]]:

        result_dict_city_details = {}

        for city in cities:

            result_dict_city_details[city] = details

        return result_dict_city_details

    def __call__(self, all_paragraphs: List[bs4.element.ResultSet],
                      all_headings: List[bs4.element.ResultSet],
                      all_locations: List[bs4.element.ResultSet]) -> Dict[str, List[str]]:

        ap_details = [k.text for i, j in enumerate(all_paragraphs) for k in j]
        price_details = [match for i, j in enumerate(all_headings) for k in j for match in
                         re.findall(r'\d+\,\d+', k.text)]
        city_details = [match for k in all_locations for match in re.findall(r'\b(?!\bCity\b)\w+\b', k[2].text)]

        result_dict_apartment_details = self.extract_apartment_details(Scraper.APARTMENT_DETAILS[0:7], ap_details)
        result_dict_price_details = self.extract_price([Scraper.APARTMENT_DETAILS[7]], price_details)
        result_dict_city_details = self.extract_city([Scraper.APARTMENT_DETAILS[8]], city_details)

        return {**result_dict_apartment_details,
                **result_dict_price_details,
                **result_dict_city_details}









