import re
import time

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from typing import Optional
from lxml import etree

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class MarketplacePriceParser:

    def __init__(self, product_url: str, articuls: list[int], price_element_xpath: str):
        '''_summary_

        Args:
            product_url (str): URL-адрес товара на сайте в соответствии 
            с артикулом для форматирования через .format, например: 
            https://www.wildberries.ru/catalog/{<артикул>}/detail.aspx
            articuls (list[int]): Список артикулов для парсинга
            price_element_xpath (str): Строка типа XPATH элемента, 
            в котором находится информация о товаре
        '''
        self.driver: uc.Chrome = uc.Chrome(use_subprocess=False)
        self.product_url = product_url
        self.articuls = articuls
        self.price_element_xpath = price_element_xpath

    def __del__(self):
        self.driver.close()

    def open_url_with_driver(self, url: str) -> None:
        self.driver.get(url)

    def check_if_page_is_loaded(self, delay: int = 2) -> bool:
        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, self.price_element_xpath))
            WebDriverWait(self.driver, delay).until(element_present)
            return True
        except TimeoutException:
            return False

    def get_soup_from_driver_page(self) -> BeautifulSoup:
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        return soup

    def open_url_with_driver_and_get_its_soup(self, url: str) -> Optional[BeautifulSoup]:
        self.open_url_with_driver(url)

        if not self.check_if_page_is_loaded(5):
            return None

        return self.get_soup_from_driver_page()

    def get_url_of_product(self, articul: int) -> str:
        return self.product_url.format(articul)

    def parse_price_from_soup(self, soup: BeautifulSoup) -> float:
        body = soup.find("body")
        dom = etree.HTML(str(body))
        price_text = dom.xpath(self.price_element_xpath)[0].text
        price = float(re.sub("[^0-9]", "", price_text))

        return price

    def parse_products_prices(self) -> dict[int, float]:
        prices = dict()

        for articul in self.articuls:
            product_url = self.get_url_of_product(articul)
            product_soup = self.open_url_with_driver_and_get_its_soup(
                product_url)

            if not product_soup:
                continue

            price = self.parse_price_from_soup(product_soup)
            prices[articul] = price

        return prices


def ozon_price_parser(*articuls: int) -> dict[int, float]:
    parser = MarketplacePriceParser(
        product_url='https://www.ozon.ru/product/{}',
        price_element_xpath='//div[1]/div[4]/div[3]/div[2]/div[1]/div[3]/div/div[1]/div/div/div[1]/div[2]/div/div[1]/span[1]',
        articuls=articuls,
    )
    prices = parser.parse_products_prices()

    return prices


def wildberries_price_parser(*articuls: int) -> dict[int, float]:
    parser = MarketplacePriceParser(
        product_url='https://www.wildberries.ru/catalog/{}/detail.aspx',
        price_element_xpath='//div[3]/div[13]/div/div[1]/div[2]/div/div/div/p/span/ins',
        articuls=articuls,
    )
    prices = parser.parse_products_prices()

    return prices


def main():

    prices = ozon_price_parser(526778267)

    for articul, price in prices.items():
        print('[{}]: {}'.format(articul, price))


if __name__ == '__main__':
    main()
    # parse_wb()
