from fastapi import APIRouter
from workshop.api.user import user_operation_router
from workshop.api.customers import customer_operation_router
from workshop.api.order import order_operation_router

router = APIRouter()
router.include_router(user_operation_router)
router.include_router(customer_operation_router)
router.include_router(order_operation_router)