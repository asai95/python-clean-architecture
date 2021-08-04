from typing import Type, Tuple

from clean_architecture.bases.abstract.bases import UseCaseRequestBase, BaseFactory
from clean_architecture.interfaces import IRepo, IUseCase, IService


class RepoFactory(BaseFactory[Type[IRepo]]):
    pass


class UseCaseFactory(BaseFactory[Tuple[Type[IUseCase], Type[UseCaseRequestBase]]]):
    pass


class ServiceFactory(BaseFactory[Type[IService]]):
    pass
