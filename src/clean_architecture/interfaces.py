from abc import ABC, abstractmethod
from typing import Any, List, TypeVar, Generic, Type, NoReturn

T = TypeVar('T')
T2 = TypeVar('T2')


class IDBSession(ABC):
    @abstractmethod
    def commit(self):
        pass


class IRepo(ABC, Generic[T]):

    @classmethod
    @abstractmethod
    def from_domain(cls, domain_obj: Type[T]) -> Any:
        pass

    @classmethod
    @abstractmethod
    def to_domain(cls, orm_obj: Any) -> Type[T]:
        pass

    @classmethod
    @abstractmethod
    def get(cls, internal_id: int) -> T:
        pass

    @classmethod
    @abstractmethod
    def get_all(cls) -> List[T]:
        pass

    @classmethod
    @abstractmethod
    def insert(cls, domain_obj) -> T:
        pass

    @classmethod
    @abstractmethod
    def update(cls, domain_obj) -> T:
        pass

    @classmethod
    @abstractmethod
    def delete(cls, domain_obj) -> T:
        pass


class IFactory(ABC, Generic[T]):
    @classmethod
    @abstractmethod
    def register(cls, obj: Type[T], name: str) -> NoReturn:
        pass

    @classmethod
    @abstractmethod
    def get(cls, name: str) -> Type[T]:
        pass


class IUseCase(Generic[T, T2], ABC):
    @classmethod
    @abstractmethod
    def execute(cls, request: T) -> T2:
        pass


class IService(ABC, Generic[T]):
    @classmethod
    @abstractmethod
    def run(cls, *args, **kwargs) -> T:
        pass
