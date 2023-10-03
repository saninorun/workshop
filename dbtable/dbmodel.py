import enum
import datetime
import sqlalchemy

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker



class Base(DeclarativeBase):
    pass

class UserBD(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name = mapped_column(sqlalchemy.String(100), nullable=False)
    last_name = mapped_column(sqlalchemy.String(100), nullable=False)
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)

    __table_args__ = (
        sqlalchemy.UniqueConstraint('first_name', 'last_name', name='uniqueuser'),
        )

    
class ProductType(enum.Enum):
    tea = 'Чай'
    coffee = 'Кофе'
    perfume = 'Парфюм'

class CustomerBD(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name = mapped_column(sqlalchemy.String(100), nullable=False)
    last_name = mapped_column(sqlalchemy.String(100), nullable=False)
    otchestvo = mapped_column(sqlalchemy.String(100), nullable=False)
    email = mapped_column(sqlalchemy.String(100), nullable=False, unique=True)
    telefon = mapped_column(sqlalchemy.Integer(), nullable=False, unique=True)
    created_on = mapped_column(sqlalchemy.DateTime(), default=datetime.datetime.now)
    updated_on = mapped_column(sqlalchemy.DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)
    is_active: Mapped[bool] = mapped_column(default=True)

    __table_args__ = (
        sqlalchemy.UniqueConstraint('first_name', 'last_name', 'otchestvo', name='uniquecustomer'),
        )

class DiscountCardsBD(Base):
    __tablename__ = 'discountcards'

    id: Mapped[int] = mapped_column(primary_key=True)
    cardnumber: Mapped[int] = mapped_column(nullable=False, unique=True)
    discount: Mapped[int] = mapped_column(nullable=False)
    is_active_for_use: Mapped[bool] = mapped_column(default=True)


class DiscountCardsHistoryBD(Base):
    __tablename__ = 'historycard'

    id: Mapped[int] = mapped_column(primary_key=True)
    cardnumber_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('discountcards.id'))
    customer_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('customers.id'))
    date_start_use = mapped_column(sqlalchemy.DateTime(), default=datetime.datetime.now)
    date_stop_use = mapped_column(sqlalchemy.DateTime())
    customer: Mapped['CustomerBD'] = relationship()
    card: Mapped['DiscountCardsBD'] = relationship()

class ProductBD(Base):
    __tablename__ = 'products'

    id = mapped_column(sqlalchemy.Integer(), primary_key=True)
    categori: Mapped[ProductType] = mapped_column(nullable=False)
    product_name = mapped_column(sqlalchemy.String(20), nullable=False, unique=True)

class ProductPriceBD(Base):
    __tablename__='productprice'

    id = mapped_column(sqlalchemy.Integer(), primary_key=True)
    product_name_id = mapped_column(sqlalchemy.Integer(), sqlalchemy.ForeignKey('products.id'), nullable=False)
    product_price = mapped_column(sqlalchemy.Integer(), nullable=False)
    price_start_date= mapped_column(sqlalchemy.Date(), default=datetime.datetime.now)
    product_name: Mapped['ProductBD'] = relationship()

    __table_args__ = (
        sqlalchemy.UniqueConstraint('product_name_id', 'price_start_date', name='uniqueprice'),
        )

class OrderBD(Base):
    __tablename__ = 'orders'

    id = mapped_column(sqlalchemy.Integer(), primary_key=True)
    customer_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('customers.id'), nullable=True)
    order_date = mapped_column(sqlalchemy.DateTime(), nullable=False, default=datetime.datetime.now)
    customer: Mapped['CustomerBD'] = relationship()
    items: Mapped[list['OrderItemBD']] = relationship()

class OrderItemBD(Base):
    __tablename__ = 'itemorder'

    id = mapped_column(sqlalchemy.Integer(), primary_key=True)
    order_number: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('orders.id'), nullable=False)
    product_name_id = mapped_column(sqlalchemy.Integer(), sqlalchemy.ForeignKey('products.id'))
    discount_card: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('discountcards.id'), nullable=True)
    product_price = mapped_column(sqlalchemy.Integer(), nullable=False)
    item_quantity = mapped_column(sqlalchemy.Integer(), nullable=False)
    total_cost: Mapped[float] = mapped_column(nullable=False)  
    product: Mapped['ProductBD'] = relationship()
    card: Mapped['DiscountCardsBD'] = relationship()