from typing import Optional, TypeVar, Dict, Type
from pydantic import BaseModel

from clean_architecture.interfaces import IFactory, IRepo, IService, IDBSession

FactoryObject = TypeVar('FactoryObject')


class BaseFactory(IFactory[FactoryObject]):
    container: Dict[str, FactoryObject] = {}

    @classmethod
    def register(cls, obj: FactoryObject, name: str):
        cls.container[name] = obj

    @classmethod
    def get(cls, name: str) -> FactoryObject:
        return cls.container[name]


class DomainBase(BaseModel):
    internal_id: Optional[int]

    class Config:
        orm_mode = True
        extra = 'allow'


class UseCaseRequestBase(BaseModel):
    repos: Type[IFactory[IRepo]]
    services: Type[IFactory[IService]]
    session: IDBSession

    class Config:
        arbitrary_types_allowed = True


class UseCaseResponseBase(BaseModel):

    class Config:
        arbitrary_types_allowed = True
