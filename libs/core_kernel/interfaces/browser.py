from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager

class IBrowserContext(ABC):
    """
    Abstract interface for browser automation contexts.
    Allows swapping Playwright for Selenium, Puppeteer, or Android ADB.
    """
    
    @abstractmethod
    async def navigate(self, url: str):
        """Navigate to a URL."""
        pass

    @abstractmethod
    async def get_cookies(self) -> Dict[str, str]:
        """Return current cookies as a dictionary."""
        pass
    
    @abstractmethod
    async def close(self):
        """Close the browser context."""
        pass

class BrowserFactory(ABC):
    """
    Factory to create browser contexts.
    """
    @abstractmethod
    @asynccontextmanager
    async def create_context(self, proxy: Optional[str] = None, headless: bool = True) -> IBrowserContext:
        """Provide a context manager for a browser session."""
        pass

# --- Concrete Implementation Stub (Playwright) ---

class PlaywrightBrowserFactory(BrowserFactory):
    """
    Concrete implementation using Playwright with anti-detect features (stub).
    """
    def __init__(self):
        # In a real impl, we would initialize the playwright instance here
        pass

    @asynccontextmanager
    async def create_context(self, proxy: Optional[str] = None, headless: bool = True):
        # Stub implementation
        print(f"DEBUG: Creating Playwright context (headless={headless}, proxy={proxy})")
        
        class StubContext(IBrowserContext):
            async def navigate(self, url: str):
                print(f"DEBUG: Navigating to {url}")
            
            async def get_cookies(self):
                return {"stub_cookie": "true"}
            
            async def close(self):
                print("DEBUG: Closing context")

        yield StubContext()
