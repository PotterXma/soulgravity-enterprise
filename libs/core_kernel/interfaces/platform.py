from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Type
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

# --- Value Objects ---

class PlatformCredentials(BaseModel):
    model_config = ConfigDict(extra="allow")  # Allow arbitrary credentials
    username: Optional[str] = None
    password: Optional[str] = None
    cookies: Optional[Dict[str, str]] = None
    token: Optional[str] = None

class AuthSession(BaseModel):
    is_active: bool
    cookies: Dict[str, str]
    expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class TrendItem(BaseModel):
    platform_id: str
    title: str
    content: Optional[str] = None
    author: str
    url: str
    metrics: Dict[str, Any] = Field(default_factory=dict)
    scraped_at: datetime = Field(default_factory=datetime.utcnow)

class PublishPayload(BaseModel):
    title: str
    content: str
    media_urls: List[str] = Field(default_factory=list)
    topics: List[str] = Field(default_factory=list)
    location: Optional[str] = None
    schedule_time: Optional[datetime] = None

class PublishResult(BaseModel):
    success: bool
    post_id: Optional[str] = None
    url: Optional[str] = None
    error_message: Optional[str] = None
    published_at: datetime = Field(default_factory=datetime.utcnow)

class AnalyticsSnapshot(BaseModel):
    post_id: str
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    saves: int = 0
    collected_at: datetime = Field(default_factory=datetime.utcnow)

class CookieHealth(BaseModel):
    is_valid: bool
    message: str
    needs_relogin: bool

# --- Interface ---

class BasePlatformAdapter(ABC):
    """
    Universal Platform Interface.
    All social media plugins MUST implement this class.
    """
    platform_name: str = "base"

    def __init__(self, tenant_id: str, proxy: Optional[str] = None):
        self.tenant_id = tenant_id
        self.proxy = proxy

    @abstractmethod
    async def login(self, credentials: PlatformCredentials) -> AuthSession:
        """Authenticate with the platform and return a session."""
        pass

    @abstractmethod
    async def fetch_hot_trends(self, keyword: str, limit: int = 10) -> List[TrendItem]:
        """Scrape trending content based on keywords."""
        pass

    @abstractmethod
    async def publish_content(self, payload: PublishPayload) -> PublishResult:
        """Publish content to the platform."""
        pass

    @abstractmethod
    async def get_analytics(self, post_id: str) -> AnalyticsSnapshot:
        """Retrieve engagement metrics for a specific post."""
        pass

    @abstractmethod
    async def check_cookie_health(self) -> CookieHealth:
        """Verify if current session/cookies are still valid."""
        pass
