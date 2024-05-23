from pydantic import BaseModel


class PriceSchema(BaseModel):
    price: int
