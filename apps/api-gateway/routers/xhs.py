from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any

from plugins.platforms.xiaohongshu.config import XhsConfig
from plugins.platforms.xiaohongshu.adapter import XiaohongshuAdapter
from libs.core_kernel.interfaces.platform import PlatformCredentials

router = APIRouter(prefix="/xhs", tags=["Xiaohongshu Plugin"])

class TestConfigRequest(BaseModel):
    config: XhsConfig
    tenant_id: str = "default"

class TestConfigResponse(BaseModel):
    success: bool
    message: str
    metadata: Dict[str, Any]

@router.post("/test-config", response_model=TestConfigResponse)
async def test_xhs_config(payload: TestConfigRequest):
    """
    Test a Xiaohongshu configuration by attempting to fetch the user profile.
    This does NOT save the config, just validates the cookie.
    """
    try:
        # Initialize adapter
        adapter = XiaohongshuAdapter(tenant_id=payload.tenant_id)
        
        # Prepare credentials
        creds = PlatformCredentials(
            cookies={"web_session": payload.config.cookie},
            proxy_url=payload.config.proxy_url
        )
        
        # Attempt login / health check
        session = await adapter.login(creds)
        
        return TestConfigResponse(
            success=True,
            message="Connection successful",
            metadata=session.metadata
        )
        
    except Exception as e:
        return TestConfigResponse(
            success=False,
            message=str(e),
            metadata={}
        )

# TODO: Add Scrape Trigger Endpoint
# TODO: Add Publish Trigger Endpoint
