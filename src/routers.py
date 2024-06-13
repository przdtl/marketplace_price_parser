import asyncio

from fastapi import APIRouter

from src.schemas import (PricesReturnSchema, ArticulsInputSchema)
from src.marketplace_price_parser import (
    ozon_price_parser, wildberries_price_parser)

router = APIRouter()


@router.post(
    '/ozon',
    name='get ozon products prices',
    response_model=PricesReturnSchema,
)
async def get_prices_for_ozon_products_handler(articuls_schema: ArticulsInputSchema):
    articuls = articuls_schema.articuls
    prices = ozon_price_parser(*articuls)

    return PricesReturnSchema(prices=prices)


@router.post(
    '/wildberries',
    name='get wildberries products prices',
    response_model=PricesReturnSchema,
)
async def get_prices_for_ozon_products_handler(articuls_schema: ArticulsInputSchema):
    articuls = articuls_schema.articuls
    prices = wildberries_price_parser(*articuls)

    return PricesReturnSchema(prices=prices)
