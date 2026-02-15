from abc import ABC, abstractmethod
from typing import Literal, Optional
from pydantic import BaseModel

class ProxyDTO(BaseModel):
    url: str  # comprehensive URL (e.g., http://user:pass@host:port)
    protocol: str
    region: Optional[str] = None
    is_sticky: bool = False

class IProxyProvider(ABC):
    """
    Interface for obtaining proxies for scraping.
    """
    
    @abstractmethod
    async def get_proxy(
        self, 
        protocol: str = "http", 
        strategy: Literal['sticky', 'random'] = 'random',
        session_id: Optional[str] = None
    ) -> ProxyDTO:
        """
        Get a proxy based on strategy.
        
        Args:
            protocol: 'http', 'https', 'socks5'
            strategy: 'sticky' (same IP for session_id) or 'random'
            session_id: Required if strategy is 'sticky'
        """
        pass
