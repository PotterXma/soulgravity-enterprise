from pydantic import BaseModel, Field
from typing import Literal, Optional

class XhsConfig(BaseModel):
    """
    Configuration for Xiaohongshu (Little Red Book) Plugin.
    """
    cookie: str = Field(
        ..., 
        description="The 'web_session' cookie from an authenticated browser session.",
        json_schema_extra={"help_text": "Copy 'web_session' from DevTools"}
    )
    user_agent: str = Field(
        default="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        description="The User-Agent string to use for requests. Must match the impersonation version."
    )
    proxy_url: Optional[str] = Field(
        default=None,
        description="HTTP/HTTPS proxy URL (e.g., http://user:pass@host:port)."
    )
    proxy_type: Literal["sticky", "random"] = Field(
        default="sticky",
        description="Strategy for proxy usage."
    )
    version: int = Field(default=1, description="Schema version for future migrations.")

    # Note: The 'cookie' field is encrypted at the Service layer using libs.security.encryption
