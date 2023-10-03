from fastapi import APIRouter, Depends
from ..services.ordersservices import OrderService
from ..models.order import  Order, OrderShow

order_operation_router = APIRouter(prefix='/order', tags=['Orders'])

@order_operation_router.post('/addOrder', response_model=OrderShow)
async def order(
    body: Order,
    service: OrderService = Depends(),
):
    return await service.addOrder(orderbody=body)