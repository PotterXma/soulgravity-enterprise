from typing import List
from libs.core_kernel.interfaces.platform import (
    BasePlatformAdapter, PlatformCredentials, AuthSession, TrendItem, 
    PublishPayload, PublishResult, AnalyticsSnapshot, CookieHealth
)
import asyncio

class DouyinAdapter(BasePlatformAdapter):
    platform_name = "douyin"

    async def login(self, credentials: PlatformCredentials) -> AuthSession:
        return AuthSession(is_active=True, cookies={"dy_session": "mock_cookie"})

    async def fetch_hot_trends(self, keyword: str, limit: int = 10) -> List[TrendItem]:
        return [
            TrendItem(
                platform_id=f"dy_{i}",
                title=f"Douyin Video {keyword} {i}",
                author="Creator888",
                url=f"https://douyin.com/video/{i}"
            )
            for i in range(limit)
        ]

    async def publish_content(self, payload: PublishPayload) -> PublishResult:
        return PublishResult(success=True, post_id="dy_post_777")

    async def get_analytics(self, post_id: str) -> AnalyticsSnapshot:
        return AnalyticsSnapshot(post_id=post_id, views=5000, likes=200)

    async def check_cookie_health(self) -> CookieHealth:
        return CookieHealth(is_valid=True, message="Healthy", needs_relogin=False)
