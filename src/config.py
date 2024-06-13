from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Product urls
    OZON_PRODUCT_URL: str = 'https://www.ozon.ru/product/{}'
    WILDBERRIES_PRODUCT_URL: str = 'https://www.wildberries.ru/catalog/{}/detail.aspx'

    # Price element xpaths
    OZON_PRICE_ELEMENT_XPATH: str = '//div[1]/div[4]/div[3]/div[2]/div[1]/div[3]/div/div[1]/div/div/div[1]/div[2]/div/div[1]/span[1]'
    WILDBERRIES_PRICE_ELEMENT_XPATH: str = '//div[3]/div[13]/div/div[1]/div[2]/div/div/div/p/span/ins'

    model_config = SettingsConfigDict(env_file='.env')
