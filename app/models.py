from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from app.db import Base


class BeerORM(Base):
    __tablename__: str = 'beer'
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(80), unique=True, nullable=False)
    tagline: str = Column(String(120), )


class BeerModel(BaseModel):
    id: int
    name: str
    tagline: str

    class Config:
        orm_mode: bool = True
        orm_model = BeerORM


class BeerList(BaseModel):
    __root__: list[BeerModel]

    class Config:
        orm_mode: bool = True
        orm_model = BeerORM
