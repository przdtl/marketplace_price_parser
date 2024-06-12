import re

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from typing import Sequence, Optional
from lxml import etree

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class SeleiumParser:

    def __init__(self):
        self.driver: uc.Chrome = uc.Chrome(use_subprocess=True, headless=True)
        self._element_located = None

    def __del__(self):
        self.driver.close()

    @property
    def element_located(self):
        return self._element_located

    @element_located.setter
    def element_located(self, e_l: tuple[str, str]):
        self._element_located = e_l

    def get_driver(self) -> WebDriver:
        return self.driver

    def open_url_with_driver(self, url: str) -> WebDriver:
        self.driver.get(url)

    def check_if_page_is_loaded(self, delay: int = 2) -> bool:
        try:
            element_present = EC.presence_of_element_located(
                self.element_located or ('', ''))
            WebDriverWait(self.driver, delay).until(element_present)
            return True
        except TimeoutException:
            return False

    def get_soup_from_driver_page(self) -> BeautifulSoup:
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        return soup


def get_soup_from_driver_page_if_page_is_loaded(parser: SeleiumParser, delay: int) -> Optional[BeautifulSoup]:
    if not parser.check_if_page_is_loaded(delay):
        return None

    return parser.get_soup_from_driver_page()


def open_url_with_driver_and_get_its_soup(parser: SeleiumParser, url: str, element_present: tuple[str, str]) -> Optional[BeautifulSoup]:
    parser.open_url_with_driver(url)
    parser.element_located = element_present

    return get_soup_from_driver_page_if_page_is_loaded(parser, delay=2)


def get_ozon_products_urls_by_articuls(*articuls: int) -> Sequence[str]:
    ozon_product_url = 'https://www.ozon.ru/product/'
    urls = []

    for articul in articuls:
        urls.append(ozon_product_url + str(articul))

    return urls


def get_ozon_products_prices_by_articuls(*articuls: int) -> Sequence[float]:
    urls = get_ozon_products_urls_by_articuls(*articuls)

    xpath_expr = '//span[contains(text(), "без Ozon Карты")]'
    ozon_element_present = (By.XPATH, xpath_expr)
    prices = []

    parser = SeleiumParser()

    for url in urls:
        product_soup = open_url_with_driver_and_get_its_soup(
            parser, url, ozon_element_present
        )

        if not product_soup:
            prices.append(-1)
            continue

        body = product_soup.find("body")

        dom = etree.HTML(str(body))
        xpath_str = '//span[contains(text(), "без Ozon Карты")]/../../div[1]/span[1]'
        price_text = dom.xpath(xpath_str)[0].text

        price = float(re.sub("[^0-9]", "", price_text))

        prices.append(price)

    return prices


def main():
    prices = get_ozon_products_prices_by_articuls(
        674840143,  # 249 р
        1584980317,  # 464 р
        1193449115,  # 1799 р
    )

    for price in prices:
        print(price)


if __name__ == '__main__':
    main()
