import sys
import os
import asyncio

# Ensure current dir is in path
sys.path.insert(0, os.getcwd())

async def verify():
    print("--- Phase 2 Verification ---")
    
    # 1. Telemetry Import
    try:
        from libs.core_kernel.telemetry import get_correlation_id
        cid = get_correlation_id()
        print(f"✅ Telemetry: Correlation ID generated: {cid}")
    except Exception as e:
        print(f"❌ Telemetry Failed: {e}")

    # 2. Proxy Provider
    try:
        from libs.infra_net.simple_proxy import SimpleProxyProvider
        # Mock env var
        os.environ["PROXY_LIST"] = "http://user:pass@1.1.1.1:8080"
        provider = SimpleProxyProvider()
        proxy = await provider.get_proxy()
        print(f"✅ Proxy: Got proxy {proxy.url}")
    except Exception as e:
        print(f"❌ Proxy Failed: {e}")

    # 3. Polymorphic Config
    try:
        from libs.infra_db.models.platform_account import PlatformAccount, PlatformConfigType
        from plugins.platforms.xiaohongshu.config import XiaohongshuConfig
        from pydantic import TypeAdapter

        print("✅ Models: PlatformAccount imported")

        # Test Pydantic Polymorphism
        config_data = {
            "platform_name": "xiaohongshu",
            "cookie": "test_cookie",
            "user_agent": "Mozilla/5.0"
        }
        
        adapter = TypeAdapter(PlatformConfigType)
        model = adapter.validate_python(config_data)
        
        if isinstance(model, XiaohongshuConfig):
             print(f"✅ Config: Polymorphism worked! Got {type(model).__name__}")
        else:
             print(f"❌ Config: Polymorphism failed, got {type(model)}")

    except Exception as e:
        print(f"❌ Config Failed: {e}")

    # 4. Celery Import
    try:
        from apps.worker_scraper import celery_config
        print("✅ Celery: Config imported")
    except Exception as e:
        print(f"❌ Celery Failed: {e}")

if __name__ == "__main__":
    asyncio.run(verify())
