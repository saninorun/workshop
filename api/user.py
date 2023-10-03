from fastapi import APIRouter, Depends, UploadFile, File
from workshop.models.user import    CreateUser, CreateUserShow, AddCard, AddCardShow,\
                                    Product, ProductShow, ProductPrice, ProductPriceShow
from workshop.services.userservices import UserService
from workshop.services.csv import GenerateCSV

user_operation_router = APIRouter(prefix='/user', tags=['User'])

@user_operation_router.post('/createUser', response_model=CreateUserShow)
async def createUser(
    body: CreateUser,
    userservice: UserService = Depends()
    ) -> CreateUserShow:
    return await userservice.userCreate(body)

@user_operation_router.post('/addCard', response_model=list[AddCardShow])
async def addCards(
    body: list[AddCard],
    userservice: UserService = Depends()
    ) -> list[AddCardShow]:
    return await userservice.addCard(body)

@user_operation_router.post('/newProduct', response_model= list[ProductShow])
async def newProduct(
    item: list[Product],
    userservice: UserService = Depends(),
) -> ProductShow:
    return await userservice.addItem(itembody = item)

@user_operation_router.post('/addPrice')
async def productPrice(
    body: list[ProductPrice],
    userservice: UserService = Depends(),
):
    return await userservice.addPrice(itemprice=body)

@user_operation_router.post('/importCsvProductPrice')
async def importCsv(
    file: UploadFile = File(...),
    userservice: GenerateCSV = Depends(),
):
    return await userservice.importCsvProductPrice(file = file.file)
