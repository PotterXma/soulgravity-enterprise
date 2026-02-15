from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from libs.infra_db.base import Base, TenantMixin

ModelType = TypeVar("ModelType", bound=Base)

class GenericRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    def _get_tenant_id(self) -> str:
        tid = TenantMixin.current_tenant()
        if not tid:
            raise ValueError("Tenant ID context is missing")
        return tid

    async def get(self, id: Any) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id)
        if issubclass(self.model, TenantMixin):
            stmt = stmt.where(self.model.tenant_id == self._get_tenant_id())
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        if issubclass(self.model, TenantMixin):
            stmt = stmt.where(self.model.tenant_id == self._get_tenant_id())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, **kwargs) -> ModelType:
        if issubclass(self.model, TenantMixin):
            kwargs['tenant_id'] = self._get_tenant_id()
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: Any, **kwargs) -> Optional[ModelType]:
        stmt = update(self.model).where(self.model.id == id).values(**kwargs).returning(self.model)
        if issubclass(self.model, TenantMixin):
            stmt = stmt.where(self.model.tenant_id == self._get_tenant_id())
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalars().first()

    async def delete(self, id: Any) -> bool:
        stmt = delete(self.model).where(self.model.id == id)
        if issubclass(self.model, TenantMixin):
            stmt = stmt.where(self.model.tenant_id == self._get_tenant_id())
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0
