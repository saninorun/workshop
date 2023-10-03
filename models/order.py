import re
import enum
from datetime import date
from pydantic import BaseModel, EmailStr, validator, ConfigDict
from fastapi import HTTPException, status


LETTER_MATCH_PATTERN = re.compile(r'^[а-яА-Яa-zA-Z\-]+$')
ERROR_INPUT_USER = HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Ошибка! Для ввода требуется использовать только алфавитные символы!'
            )

class Show(BaseModel):
    model_config = ConfigDict(from_attributes = True)

class OrderItem(BaseModel):
    product_name: str
    item_quantity: int

    @validator('product_name')
    def upperName(cls, value):
        if not value or not LETTER_MATCH_PATTERN.match(value):
            raise ERROR_INPUT_USER
        return value.capitalize()

class Order(BaseModel):
    last_name: str|None
    cardnumber: int|None
    item_order: list[OrderItem]
    
    @validator('last_name')
    def upperName(cls, value):
        if not value or not LETTER_MATCH_PATTERN.match(value):
            raise ERROR_INPUT_USER
        return value.capitalize()

class OrderItemShow(BaseModel):
    item_name: str
    item_quantity: int
    item_cost_one: int
    item_total_discount: int|None
    item_total_cost: int

class OrderShow(Show):
    id: int
    first_name: str|None
    last_name: str|None
    cardnumber: int|None
    total_cost_order: int
    items_order: list[OrderItemShow]