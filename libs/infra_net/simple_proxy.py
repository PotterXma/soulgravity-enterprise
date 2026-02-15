import os
import random
import hashlib
from typing import List, Literal, Optional
from libs.core_kernel.interfaces.proxy_provider import IProxyProvider, ProxyDTO

class SimpleProxyProvider(IProxyProvider):
    """
    Reference implementation: Reads proxies from environment variable or static list.
    Env format: PROXY_LIST="http://u:p@ip:port,http://u:p@ip2:port2"
    """
    def __init__(self, proxy_list: Optional[List[str]] = None):
        if proxy_list:
            self._proxies = proxy_list
        else:
            env_val = os.getenv("PROXY_LIST", "")
            self._proxies = [p.strip() for p in env_val.split(",") if p.strip()]

    async def get_proxy(
        self, 
        protocol: str = "http", 
        strategy: Literal['sticky', 'random'] = 'random',
        session_id: Optional[str] = None
    ) -> ProxyDTO:
        if not self._proxies:
            raise ValueError("No proxies available in configuration")

        if strategy == 'sticky' and session_id:
            # Hash-based selection for stickiness
            hash_val = int(hashlib.md5(session_id.encode()).hexdigest(), 16)
            proxy_url = self._proxies[hash_val % len(self._proxies)]
            is_sticky = True
        else:
            # Random selection
            proxy_url = random.choice(self._proxies)
            is_sticky = False

        return ProxyDTO(
            url=proxy_url,
            protocol=protocol,
            is_sticky=is_sticky
        )
