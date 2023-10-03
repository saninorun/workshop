import re
import enum
from datetime import date
from pydantic import BaseModel, EmailStr, validator, ConfigDict
from fastapi import HTTPException, status


LETTER_MATCH_PATTERN = re.compile(r'^[а-яА-Яa-zA-Z\-]+$')
ERROR_INPUT_USER = HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Ошибка! Для ввода ФИО требуется использовать только алфавитные символы!'
            )

class Show(BaseModel):
    model_config = ConfigDict(from_attributes = True)

class CreateCustomer(BaseModel):
    first_name: str
    last_name: str
    otchestvo: str
    email: EmailStr
    telefon: int
    created_on: date|None
    is_active: bool|None = True
    

    @validator('first_name', 'last_name', 'otchestvo')
    def validate_first_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise ERROR_INPUT_USER
        return value.title()
    
class CreateCustomerShow(Show, CreateCustomer):
    id: int
    cardnumber: int
    discount: int