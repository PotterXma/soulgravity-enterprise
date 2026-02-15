from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy import String, DateTime, select
from datetime import datetime
from contextvars import ContextVar
from typing import Optional

# Global context variable for Tenant ID
# This should be set by middleware
tenant_context: ContextVar[Optional[str]] = ContextVar("tenant_id", default=None)

class Base(DeclarativeBase):
    pass

class TenantMixin:
    """
    Mixin that adds tenant_id column and automatic filtering.
    """
    @declared_attr
    def tenant_id(cls) -> Mapped[str]:
        return mapped_column(String, index=True, nullable=False)

    @classmethod
    def current_tenant(cls) -> Optional[str]:
        return tenant_context.get()

# Note: Automatic filtering usually requires a custom Session or Event listener.
# Ideally, we implement it in the Repository layer to keep models pure,
# but we can also use SQLAlchemy events here if desired.
# For this design, we will enforce tenant filtering in the GenericRepository.
