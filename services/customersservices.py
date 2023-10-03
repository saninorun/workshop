from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.customers import CreateCustomer, CreateCustomerShow
from ..dbtable.dbmodel import CustomerBD, DiscountCardsHistoryBD
from ..core.database import get_session
from ..services.queries import Query


class CustomerService:
    
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def createCustomer(self, new_customer: CreateCustomer) -> CreateCustomerShow:
        new_customer = CustomerBD(**new_customer.model_dump())
        async with self.session.begin():
            rezult = await self.session.execute(Query.query_card_for_newcustomer)
            rezult = rezult.first()
            if not rezult:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail="Не найдено ни одного свободного номера дисконтной карты! "\
                        "Все розданы. Необходимо внести в справочник дисконтных карт дополнительные номера карт!"
                    )
            self.session.add(new_customer)
            self.session.add(DiscountCardsHistoryBD(customer=new_customer, card = rezult[0]))
        
        new_customer = CreateCustomerShow(
                id = new_customer.id,
                first_name = new_customer.first_name,
                last_name = new_customer.last_name,
                otchestvo = new_customer.otchestvo,
                email = new_customer.email,
                telefon = new_customer.telefon,
                created_on = new_customer.created_on,
                cardnumber = rezult[0].cardnumber,
                discount = rezult[0].discount,
            ) 
        return new_customer
    
    async def deleteCustomer(self, telefon: int) -> None:
        pass