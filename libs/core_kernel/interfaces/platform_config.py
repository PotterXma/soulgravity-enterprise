from pydantic import BaseModel, Field
from typing import Literal

class BasePlatformConfig(BaseModel):
    """
    Base configuration for all platforms.
    Polymorphic deserialization is handled via the `platform_name` discriminator.
    """
    platform_name: str
    is_enabled: bool = True
    daily_post_limit: int = Field(default=5, ge=0)
    
    # Common settings for all platforms
    proxy_strategy: Literal['sticky', 'random'] = 'random'
