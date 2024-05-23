from fastapi import APIRouter

from src.schemas import PriceSchema

router = APIRouter()


@router.get(
    '/price',
    name='get price',
    response_model=PriceSchema,
)
async def get_product_price_by_articul_router(articul: int):
    return PriceSchema(price=10)
