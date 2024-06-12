import asyncio

from fastapi import APIRouter

from src.schemas import PriceSchema, SomeArticulsSchema, SomePricesSchema
from src.ozon_parser_service import get_ozon_products_prices_by_articuls

router = APIRouter()


@router.get(
    '/price',
    name='get price',
    response_model=PriceSchema,
)
async def get_product_price_by_articul_router(articul: int):
    prices = get_ozon_products_prices_by_articuls(articul)
    price = prices[0]

    return PriceSchema(price=price)


@router.post(
    '/price',
    name='get some prices',
    response_model=SomePricesSchema,
)
async def get_products_prices_by_articuls_list(articuls_schema: SomeArticulsSchema):
    articuls = articuls_schema.articuls
    prices = get_ozon_products_prices_by_articuls(*articuls)

    return SomePricesSchema(prices=prices)
