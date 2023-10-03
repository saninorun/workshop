from fastapi import APIRouter, Depends
from workshop.models.customers import CreateCustomer, CreateCustomerShow
from ..services.customersservices import CustomerService

customer_operation_router = APIRouter(prefix='/customer', tags=['Customer'])

@customer_operation_router.post('/newCustomer', response_model= CreateCustomerShow)
async def newCustomer(
    body: CreateCustomer, 
    service: CustomerService = Depends(),
) -> CreateCustomerShow:
    return await service.createCustomer(body)

@customer_operation_router.delete("/deleteCustomer/{telefon}")
async def delete_operation(
    telefon: int,
    service: CustomerService = Depends(),
    ) -> None:
    await service.deleteCustomer(telefon = telefon)
    return "Покупатель удален!"