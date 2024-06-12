from pydantic import BaseModel


class PriceSchema(BaseModel):
    price: float


class SomePricesSchema(BaseModel):
    prices: list[float]


class SomeArticulsSchema(BaseModel):
    articuls: list[int]
