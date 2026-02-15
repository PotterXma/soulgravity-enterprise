import asyncio
import json
from typing import List, Dict, Any, Optional
from curl_cffi.requests import AsyncSession, Response

from libs.core_kernel.interfaces.platform import (
    BasePlatformAdapter, PlatformCredentials, AuthSession, TrendItem, 
    PublishPayload, PublishResult, AnalyticsSnapshot, CookieHealth
)
from plugins.platforms.xiaohongshu.signing import XhsSigner
from plugins.platforms.xiaohongshu.config import XhsConfig

class PlatformAntiSpiderError(Exception):
    """Raised when WAF/Anti-Spider blocks the request (461, 462)."""
    pass

class PlatformAuthError(Exception):
    """Raised when authentication fails (401, 403)."""
    pass

class XiaohongshuAdapter(BasePlatformAdapter):
    platform_name = "xiaohongshu"
    BASE_URL = "https://edith.xiaohongshu.com"
    
    def __init__(self, tenant_id: str, proxy: Optional[str] = None):
        super().__init__(tenant_id, proxy)
        self.session: Optional[AsyncSession] = None
        self.config: Optional[XhsConfig] = None

    async def _init_session(self, credentials: PlatformCredentials) -> None:
        """Initialize curl_cffi AsyncSession with Chrome impersonation."""
        # Convert credentials to internal config model if needed
        # For now assume credentials.cookies contains the necessary components
        
        proxy = self.proxy
        # Check if proxy is in credentials (override)
        if hasattr(credentials, "proxy_url") and credentials.proxy_url:
            proxy = credentials.proxy_url

        self.session = AsyncSession(
            impersonate="chrome110",
            proxies={"http": proxy, "https": proxy} if proxy else None,
            timeout=30
        )
        
        if credentials.cookies:
            self.session.cookies.update(credentials.cookies)
            
        # Set default headers
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "Content-Type": "application/json;charset=UTF-8",
            "Referer": "https://www.xiaohongshu.com/",
            "Origin": "https://www.xiaohongshu.com"
        })

    async def _request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        """Centralized request method with signing and error handling."""
        if not self.session:
            raise RuntimeError("Session not initialized. Call login() first.")

        # Sign the request
        # Note: XHS signing usually targets the path + params
        uri = endpoint
        if params:
            # Simple query param string construction for signing (mock logic)
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            uri = f"{endpoint}?{query_string}"
            
        headers = XhsSigner.sign_request(uri, data)
        self.session.headers.update(headers)
        
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            response: Response = await self.session.request(
                method=method, 
                url=url, 
                json=data, 
                params=params
            )
        except Exception as e:
            # Network errors
            raise RuntimeError(f"Network error during XHS request: {str(e)}") from e

        # Anti-Spider Checks
        if response.status_code in [461, 462]:
            raise PlatformAntiSpiderError(f"Trapped by XHS WAF. Status: {response.status_code}")
        
        if response.status_code == 401:
            raise PlatformAuthError("Cookie expired or invalid.")
            
        if response.status_code != 200:
            raise RuntimeError(f"XHS API Error: {response.status_code} - {response.text}")
            
        try:
            return response.json()
        except json.JSONDecodeError:
            raise RuntimeError(f"Invalid JSON response: {response.text}")

    async def login(self, credentials: PlatformCredentials) -> AuthSession:
        """Authenticate using cookies directly."""
        await self._init_session(credentials)
        
        # Validate immediately
        health = await self.check_cookie_health()
        if not health.is_valid:
            raise PlatformAuthError(f"Login failed: {health.message}")
            
        return AuthSession(
            is_active=True,
            cookies=self.session.cookies.get_dict(), # type: ignore
            metadata=json.loads(health.message) if health.is_valid else {}
        )

    async def check_cookie_health(self) -> CookieHealth:
        """Verify session by fetching user profile."""
        if not self.session:
             # If no session exists, we can't check. 
             # In a real flow, login() is called first. 
             # If check_cookie_health is called standalone, it assumes session is ready.
             return CookieHealth(is_valid=False, message="Session not initialized", needs_relogin=True)

        try:
            # Me endpoint: /api/sns/web/v1/user/me or user/otherinfo with own ID
            # Using a known stable endpoint for validation
            res = await self._request("GET", "/api/sns/web/v1/user/me")
            
            if res.get("code") == 0 and res.get("data"):
                user_data = res["data"]
                info = {
                    "nickname": user_data.get("nickname"),
                    "user_id": user_data.get("user_id"),
                    "avatar": user_data.get("images"),
                }
                return CookieHealth(
                    is_valid=True, 
                    message=json.dumps(info), 
                    needs_relogin=False
                )
            else:
                return CookieHealth(
                    is_valid=False, 
                    message=f"API verified but returned error: {res.get('msg')}", 
                    needs_relogin=True
                )

        except PlatformAuthError:
            return CookieHealth(is_valid=False, message="Cookie expired (401)", needs_relogin=True)
        except PlatformAntiSpiderError:
            return CookieHealth(is_valid=False, message="WAF Blocked (461)", needs_relogin=True)
        except Exception as e:
            return CookieHealth(is_valid=False, message=f"Verification failed: {str(e)}", needs_relogin=True)

    async def fetch_hot_trends(self, keyword: str, limit: int = 10) -> List[TrendItem]:
        """Scrape search results."""
        if not self.session:
            raise RuntimeError("Not logged in")

        endpoint = "/api/sns/web/v1/search/notes"
        payload = {
            "keyword": keyword,
            "page": 1,
            "page_size": limit,
            "sort": "general",
            "note_type": 0 # All types
        }
        
        # Random sleep handling should happen at the service/task layer, not here
        # But for safety, adapter represents "one atomic operation"
        
        res = await self._request("POST", endpoint, data=payload)
        
        items = []
        if res.get("code") == 0 and res.get("data", {}).get("items"):
            for note in res["data"]["items"]:
                # Parse note structure
                note_data = note.get("note_card", {})
                user_data = note_data.get("user", {})
                
                items.append(TrendItem(
                    platform_id=note.get("id") or note_data.get("note_id"),
                    title=note_data.get("display_title") or note_data.get("title", "Untitled"),
                    author=user_data.get("nickname", "Unknown"),
                    url=f"https://www.xiaohongshu.com/explore/{note.get('id')}",
                    metrics={
                        "likes": note_data.get("interact_info", {}).get("liked_count", 0),
                        "type": note_data.get("type")
                    }
                ))
        return items

    async def _upload_image(self, url: str) -> str:
        """
        Upload image flow helper.
        1. Get upload config/token
        2. Upload binary
        3. Commit/Finish upload
        """
        # Mocking the complex multi-step upload flow for this iteration
        # In reality this involves PUT to oss endpoints
        # Returning a fake image_id
        await asyncio.sleep(1) # simulate network
        return f"img_id_mock_{hash(url)}"

    async def publish_content(self, payload: PublishPayload) -> PublishResult:
        """Publish a note."""
        if not self.session:
            raise RuntimeError("Not logged in")

        # 1. Upload Images
        image_ids = []
        for img_url in payload.media_urls:
            try:
                # We would need to download the image from URL first if it's remote, 
                # or assume it's a local path. 
                # For this adapter, we assume payload.media_urls are accessible.
                # Here we just mock the upload process.
                img_id = await self._upload_image(img_url)
                image_ids.append(img_id)
            except Exception as e:
                return PublishResult(success=False, error_message=f"Image upload failed: {str(e)}")

        # 2. Publish
        endpoint = "/api/sns/web/v1/feed/publish"
        publish_data = {
            "title": payload.title,
            "content": payload.content,
            "image_ids": image_ids,
            "post_type": "image", # or video
            "topics": payload.topics,
            "is_private": False
        }
        
        try:
            res = await self._request("POST", endpoint, data=publish_data)
            if res.get("code") == 0:
                 note_id = res.get("data", {}).get("note_id")
                 return PublishResult(
                     success=True, 
                     post_id=note_id, 
                     url=f"https://www.xiaohongshu.com/explore/{note_id}"
                 )
            else:
                 return PublishResult(success=False, error_message=res.get("msg"))
                 
        except Exception as e:
            return PublishResult(success=False, error_message=str(e))

    async def get_analytics(self, post_id: str) -> AnalyticsSnapshot:
        # Stub
        return AnalyticsSnapshot(post_id=post_id, views=0, likes=0)
