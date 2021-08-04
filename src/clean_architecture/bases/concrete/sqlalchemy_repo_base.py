from typing import Type, Callable, TypeVar, Any, List, Dict, Union

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy_filters import apply_filters, apply_sort, apply_pagination

from clean_architecture.bases.abstract.bases import DomainBase
from clean_architecture.interfaces import IRepo

OrmModel = TypeVar('OrmModel')


class SqlAlchemyBaseRepo(IRepo):
    orm_model: Type[OrmModel]
    domain_model: Type[DomainBase]
    session: Session

    @classmethod
    def _db_persist(cls, func: Callable, *args, **kwargs) -> DomainBase:
        try:
            obj = func(*args, **kwargs)
            cls.session.commit()
            return obj
        except SQLAlchemyError as e:
            cls.session.rollback()
            raise e
    
    @classmethod
    def from_domain(cls, domain_obj: DomainBase) -> OrmModel:
        return cls.orm_model(**domain_obj.dict())
    
    @classmethod
    def to_domain(cls, orm_obj: OrmModel) -> DomainBase:
        return cls.domain_model.from_orm(orm_obj)
    
    @classmethod
    def get(cls, internal_id: Any) -> DomainBase:
        return cls.to_domain(cls.orm_model.query.get(internal_id))
    
    @classmethod
    def get_all(cls) -> List[DomainBase]:
        return [cls.to_domain(x) for x in cls.orm_model.query.all()]
    
    @classmethod
    def orm_from_dict(cls, dict_obj: Dict) -> OrmModel:
        return cls.orm_model(**dict_obj)
    
    @classmethod
    def from_dict(cls, dict_obj: Dict) -> DomainBase:
        return cls.domain_model(**dict_obj)
    
    @classmethod
    def _update(cls, domain_obj: DomainBase) -> DomainBase:
        orm_obj = cls.from_domain(domain_obj)
        cls.session.merge(orm_obj)
        cls.session.flush()
        orm_obj = cls.orm_model.query.get(domain_obj.internal_id)
        domain_obj = cls.to_domain(orm_obj)
        return domain_obj
    
    @classmethod
    def _insert(cls, domain_obj: DomainBase) -> DomainBase:
        orm_obj = cls.from_domain(domain_obj)
        cls.session.add(orm_obj)
        cls.session.flush()
        domain_obj = cls.to_domain(orm_obj)
        return domain_obj
    
    @classmethod
    def _delete(cls, domain_obj: DomainBase) -> DomainBase:
        orm_obj = cls.orm_model.query.get(domain_obj.internal_id)
        cls.session.delete(orm_obj)
        cls.session.flush()
        domain_obj = cls.to_domain(orm_obj)
        return domain_obj
    
    @classmethod
    def update(cls, domain_obj: DomainBase, commit: bool = True) -> DomainBase:
        if not commit:
            return cls._update(domain_obj)
        return cls._db_persist(cls._update, domain_obj)
    
    @classmethod
    def insert(cls, domain_obj: DomainBase, commit: bool = True) -> DomainBase:
        if not commit:
            return cls._insert(domain_obj)
        return cls._db_persist(cls._insert, domain_obj)
    
    @classmethod
    def delete(cls, domain_obj: DomainBase, commit: bool = True) -> DomainBase:
        if not commit:
            return cls._delete(domain_obj)
        return cls._db_persist(cls._delete, domain_obj)

    @classmethod
    def query(cls, query: Union[Dict, List[Dict]] = None, sort: Dict = None, pagination: Dict = None):
        sql_query = cls.orm_model.query
        if query:
            sql_query = apply_filters(sql_query, query)
        if sort:
            sql_query = apply_sort(sql_query, sort)
        if pagination:
            sql_query, _ = apply_pagination(sql_query, **pagination)
        return [cls.to_domain(x) for x in sql_query.all()]

    @classmethod
    def count(cls):
        return cls.orm_model.query.count()
