from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from typing import Union, Annotated
from pydantic import Field, TypeAdapter

from libs.infra_db.base import Base, TenantMixin
from libs.core_kernel.interfaces.platform_config import BasePlatformConfig
from plugins.platforms.xiaohongshu.config import XhsConfig

# Define the Union of all possible configs for polymorphism
# When we have more platforms, we add them here: Union[XhsConfig, DouyinConfig, ...]
PlatformConfigType = Annotated[Union[XhsConfig], Field(discriminator='platform_name')]

class PlatformAccount(Base, TenantMixin):
    __tablename__ = "platform_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_name: Mapped[str]
    platform: Mapped[str]  # e.g. 'xiaohongshu'

    # Store polymorphic config as JSONB
    # In Pydantic V2 + SQLAlchemy 2.0, we can use a custom type or just JSONB
    # and validate in the service layer, OR use specialized libraries.
    # Here is the clean standard way:
    _config: Mapped[dict] = mapped_column("config", JSONB, nullable=False)

    @property
    def config(self) -> BasePlatformConfig:
        # Validate/Parse on read
        adapter = TypeAdapter(PlatformConfigType)
        return adapter.validate_python(self._config)

    @config.setter
    def config(self, value: BasePlatformConfig):
        # Serialize on write
        self._config = value.model_dump(mode='json')
