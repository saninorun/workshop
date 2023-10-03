import datetime
import csv 
from typing import Any
from fastapi import Depends, HTTPException, status
from sqlalchemy import select, update, and_, exc
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user import CreateUser, AddCard, ProductPrice, Product
from ..dbtable.dbmodel import UserBD, DiscountCardsBD, ProductBD, ProductPriceBD
from ..core.database import get_session
from ..core.security import AuthService
from ..services.queries import Query

class UserService(AuthService):
    
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
    
    async def userCreate(self, userbody: CreateUser) -> UserBD:
        body = userbody.model_dump()
        body.update([('password_hash', self.hash_password(userbody.password_hash))])
        new_user = UserBD(**body)
        async with self.session.begin():
            self.session.add(new_user)
        return new_user
    
    async def addCard(self, cardbody: list[AddCard]) -> list[DiscountCardsBD]:
        cards = []
        for card in cardbody:
            cards.append(DiscountCardsBD(**card.model_dump()))
        async with self.session.begin():
            self.session.add_all(cards)
        return cards
        
    async def addItem(self, itembody: list[Product]) -> list[ProductBD]:
        new_product= []
        for item in itembody:
            new_product.append(ProductBD(**item.model_dump()))
        async with self.session.begin():
            self.session.add_all(new_product)
        return new_product
             
    async def addPrice(self, *, itemprice: list[ProductPrice]):
        new_price=[]
        missing_products = []
        itemprice_for_update = []
        for item in itemprice:
            try:
                product = await self._getItem(item=item.product_name)
                productprice = ProductPriceBD(
                    product_price = item.product_price, 
                    product_name = product, 
                    price_start_date = item.price_start_date
                )
                new_price.append(productprice)
            except HTTPException:
                missing_products.append(item)
        
        for item in new_price:
            try:
                async with self.session.begin():
                    self.session.add(item)
            except exc.IntegrityError:
                itemprice_for_update.append(item)
        
        for item in itemprice_for_update:
            query = update(ProductPriceBD).where(
                and_(
                    ProductPriceBD.product_name_id == item.product_name_id,
                    ProductPriceBD.price_start_date == item.price_start_date,
                    )
                    ).values(product_price = item.product_price)
            async with self.session.begin():
                await self.session.execute(query)

        if missing_products:
            return [HTTPException(
                status_code=status.HTTP_200_OK, 
                detail='Цены на существующие товары актуализированы.'\
                    'Есть не установленные цены в связи с отсутствием товра в справочнике товаров',
                ), missing_products]
        else:
            return HTTPException(
                status_code=status.HTTP_200_OK, 
                detail='Цены на существующие товары актуализированы.',
                )            