from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float)
    count = Column(Integer)
    
    # Задание 9.1 (Пункт 6): Измените модель данных, добавив новое поле[cite: 29].
    # Раскомментируйте строку ниже ПЕРЕД созданием второй миграции:
    description = Column(String, nullable=False, server_default="Описание отсутствует")