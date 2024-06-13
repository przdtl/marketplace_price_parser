from pydantic import BaseModel


class PricesReturnSchema(BaseModel):
    prices: dict[int, float]


class ArticulsInputSchema(BaseModel):
    articuls: list[int]
