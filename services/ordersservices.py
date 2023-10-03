import datetime
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.order import Order, OrderItem, OrderShow, OrderItemShow
from ..dbtable.dbmodel import CustomerBD, ProductBD, ProductPriceBD, OrderBD, OrderItemBD, DiscountCardsBD, DiscountCardsHistoryBD
from ..core.database import get_session


class OrderService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def _getItem(self, item: str) -> ProductBD:
        query = select(ProductBD).where(ProductBD.product_name == item)
        async with self.session.begin():
            rezult = await self.session.execute(query)
            rezult = rezult.first()
            if not rezult:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail="Такого наименования товара не существует! Проверьте справочник товара."
                )
        return rezult[0]
    
    async def _getUserAndCardNumber(self, *, last_name: str, cardnumber: int):
        query = select(
            CustomerBD,
            DiscountCardsBD
            ).join(
                DiscountCardsHistoryBD.customer,
                ).join(
                    DiscountCardsHistoryBD.card,
                    ).where(
                         CustomerBD.last_name.contains(last_name) if last_name 
                         else DiscountCardsBD.cardnumber == cardnumber,
                        )
        async with self.session.begin():
            rezult = await self.session.execute(query)
            rezult = rezult.first()
            if not rezult:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail="Пользователь или карта не найдены!"
                )
        return rezult
    
    async def _getPrice(self, item: str) -> ProductPriceBD:
        query = select(  
            ProductPriceBD,                                     
            ).join_from(
                ProductBD, ProductPriceBD, ProductBD.id == ProductPriceBD.product_name_id,                   
                ).where(
                    ProductPriceBD.price_start_date <= datetime.datetime.now(),
                    ProductBD.product_name == item,
                    ).order_by(
                        ProductPriceBD.product_price.desc()
                        )
        async with self.session.begin():
            rezult = await self.session.execute(query)
            rezult = rezult.first()
            if not rezult:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail="Не назначена цена на товар! Необходимо назначиить цену в справочнике цен."
                )
        return rezult[0]

    async def addOrder(self, orderbody: Order):        
        if orderbody.last_name or orderbody.cardnumber:
            user_discountcard = await self._getUserAndCardNumber(
                last_name=orderbody.last_name, 
                cardnumber=orderbody.cardnumber,
                )           
        else:
            user_discountcard = (None, None)
        itemsorder = []
        total_cost_order = 0
        for item in orderbody.item_order:
            product = await self._getItem(item=item.product_name)
            price = await self._getPrice(item=item.product_name)
            total_cost_items = (item.item_quantity * price.product_price)*\
                         ((1-user_discountcard[1].discount/100) if user_discountcard[1] else 1)
            orderunititem = OrderItemBD(
                    product_price = price.product_price,
                    item_quantity = item.item_quantity,
                    total_cost = total_cost_items,
                    card=user_discountcard[1],
                    product = product,
                    )
            total_cost_order += total_cost_items
            itemsorder.append(orderunititem)
        addorder = OrderBD(customer = user_discountcard[0], 
                           items = itemsorder,
                           )
        async with self.session.begin():
            self.session.add(addorder)
        items_show = []
        for item in addorder.items:
            item_outer = OrderItemShow(
                item_name = item.product.product_name,
                item_quantity = item.item_quantity,
                item_cost_one = item.product_price,
                item_total_discount = (item.item_quantity * item.product_price) - item.total_cost,
                item_total_cost = item.total_cost,
                )
            items_show.append(item_outer)
        order = OrderShow(
            id = addorder.id,
            first_name = addorder.customer.first_name if addorder.customer else None,
            last_name = addorder.customer.last_name if addorder.customer else None,
            cardnumber = user_discountcard[1].cardnumber if user_discountcard[1] else None,
            total_cost_order = total_cost_order,
            items_order = items_show,
            )
        return order
