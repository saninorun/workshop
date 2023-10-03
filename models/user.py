import re
import enum
from datetime import date
from pydantic import BaseModel, EmailStr, validator, constr, ConfigDict
from fastapi import HTTPException, status


LETTER_MATCH_PATTERN = re.compile(r'^[а-яА-Яa-zA-Z\-]+$')
ERROR_INPUT_USER = HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Ошибка! Для ввода ФИО требуется использовать только алфавитные символы!'
            )

class Show(BaseModel):
     model_config = ConfigDict(from_attributes = True)

class CreateUser(BaseModel):
    first_name: str
    last_name: str
    login: str
    email: EmailStr|None = None
    password_hash: constr(min_length=8)
    
    @validator('first_name', 'last_name', 'login')
    def validate_first_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise ERROR_INPUT_USER
        return value.title()
    
class CreateUserShow(Show, CreateUser):
    id: int

class AddCard(BaseModel):
    cardnumber: int
    discount: int

class AddCardShow(Show, AddCard):
    id: int

class ProductType(str, enum.Enum):
    tea = 'Чай'
    coffee = 'Кофе'
    perfume = 'Парфюм'

class Product(BaseModel):
    categori: ProductType
    product_name: str

    @validator('product_name')
    def upperFirstProductName(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise ERROR_INPUT_USER
        return value.capitalize()

class ProductShow(Show, Product):
    id: int

class ProductPrice(BaseModel):
    product_name: str
    product_price: int
    price_start_date: date|None

    @validator('product_name')
    def upperName(cls, value):
        if not value or not LETTER_MATCH_PATTERN.match(value):
            raise ERROR_INPUT_USER
        return value.capitalize()

class ProductPriceShow(Show):
    id: int
    product_name_id: int
    product_price: int
    price_start_date: date