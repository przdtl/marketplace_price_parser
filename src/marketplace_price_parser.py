import re

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from typing import Optional
from lxml import etree

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from src.config import Settings


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
        self.driver: uc.Chrome = uc.Chrome(use_subprocess=True)
        self.product_url = product_url
        self.articuls = articuls
        self.price_element_xpath = price_element_xpath

    def __del__(self):
        self.driver.close()

    def _open_url_with_driver(self, url: str) -> None:
        self.driver.get(url)

    def _check_if_page_is_loaded(self, delay: int = 2) -> bool:
        '''
        Ожидает загрузку страницы в течении ``delay`` секунд

        Args:
            delay (int): Максимальное время ожидания загрузки страницы

        Returns:
            bool: Успешность загрузки станицы

        '''
        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, self.price_element_xpath))
            WebDriverWait(self.driver, delay).until(element_present)
            return True
        except TimeoutException:
            return False

    def _get_soup_from_driver_page(self) -> BeautifulSoup:
        '''Возвращает объект ``BeautifulSoup`` с данными о загруженной странице'''
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        return soup

    def _open_url_with_driver_and_get_its_soup(self, url: str) -> Optional[BeautifulSoup]:
        '''Открывает переданную страницу и считывает с неё объект ``BeautifulSoup``'''
        self._open_url_with_driver(url)

        if not self._check_if_page_is_loaded(5):
            return None

        return self._get_soup_from_driver_page()

    def _get_url_of_product(self, articul: int) -> str:
        '''Получает URL на товар по переданному артикулу'''
        return self.product_url.format(articul)

    def _parse_price_from_soup(self, soup: BeautifulSoup) -> float:
        '''Находит на странице элемент, хранящий в себе цену товара. Получает из него данные о цене, чистит их и возвращает'''
        body = soup.find("body")
        dom = etree.HTML(str(body))
        price_text = dom.xpath(self.price_element_xpath)[0].text
        price = float(re.sub("[^0-9]", "", price_text))

        return price

    def parse_products_prices(self) -> dict[int, float]:
        '''Получает данные о цене товаров из ``articuls``'''
        prices = dict()

        for articul in self.articuls:
            product_url = self._get_url_of_product(articul)
            product_soup = self._open_url_with_driver_and_get_its_soup(
                product_url)

            if not product_soup:
                continue

            price = self._parse_price_from_soup(product_soup)
            prices[articul] = price

        return prices


def ozon_price_parser(*articuls: int) -> dict[int, float]:
    parser = MarketplacePriceParser(
        product_url=Settings().OZON_PRODUCT_URL,
        price_element_xpath=Settings().OZON_PRICE_ELEMENT_XPATH,
        articuls=articuls,
    )
    prices = parser.parse_products_prices()

    return prices


def wildberries_price_parser(*articuls: int) -> dict[int, float]:
    parser = MarketplacePriceParser(
        product_url=Settings().WILDBERRIES_PRODUCT_URL,
        price_element_xpath=Settings().WILDBERRIES_PRICE_ELEMENT_XPATH,
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
