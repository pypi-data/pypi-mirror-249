# -*- coding: utf-8 -*-
from typing import Optional, Any, Generic, TypeVar, List

from fastapi_async_sqlalchemy import db
from pydantic import BaseModel
from sqlmodel import select, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select

from .pagination import PagingParams, Pagination, paginate

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class _ServiceMetaClass(type):
    def __new__(mcs, name, bases, attrs):
        return super().__new__(mcs, name, bases, attrs)


class BaseDAO(Generic[ModelType, CreateSchemaType, UpdateSchemaType], metaclass=_ServiceMetaClass):
    model: type[ModelType] = None
    pagination_class = None
    database = db

    def _gen_condition(self, kwargs: dict) -> List:
        conditions = []
        for field, value in kwargs.items():
            conditions.append(getattr(self.model, field) == value)
        return conditions

    async def get_one(
            self, session: Optional[AsyncSession] = None, **kwargs
    ) -> ModelType | None:
        db_session = session or self.database.session
        query = select(self.model).where(*self._gen_condition(kwargs))
        response = await db_session.execute(query)
        return response.scalar_one_or_none()

    async def get_by_id(self, pk: Any) -> ModelType | None:
        return await self.get_one(id=pk)

    async def with_pagination(
            self,
            query: ModelType | Select[ModelType] | None = None,
            params: PagingParams = PagingParams()
    ) -> Pagination[ModelType]:
        """ 分页查询 """
        response = await paginate(
            self.database.session,
            query=query,
            params=params
        )
        return response

    async def create(
            self,
            data: CreateSchemaType | ModelType,
            session: Optional[AsyncSession] = None
    ) -> ModelType:
        """创建对象"""
        db_session = session or self.database.session
        data_model = self.model.from_orm(data)

        try:
            db_session.add(data_model)
            await db_session.commit()
        except Exception as e:
            await db_session.rollback()
            raise e
        await db_session.refresh(data_model)
        return data_model
