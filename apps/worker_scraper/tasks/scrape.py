from apps.worker_scraper.celery_app import app
from libs.core_kernel.plugin_loader import PluginManager
import asyncio

@app.task
def scrape_platform_task(platform_name: str, tenant_id: str, keyword: str):
    print(f"INFO: Starting scrape task for {platform_name} (tenant={tenant_id})")
    
    # In a real sync task, we'd run async code via asyncio.run or similar
    # or use celery-pool-asyncio if supported.
    # For now, simplistic sync wrapper:
    
    async def run():
        pm = PluginManager.instance()
        pm.discover()  # Ensure plugins are loaded in worker process
        
        adapter_cls = pm.get_adapter_class(platform_name)
        if not adapter_cls:
            print(f"ERROR: No adapter found for {platform_name}")
            return
        
        adapter = adapter_cls(tenant_id=tenant_id)
        results = await adapter.fetch_hot_trends(keyword=keyword)
        print(f"SUCCESS: Scraped {len(results)} items from {platform_name}")
        return [item.model_dump() for item in results]

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    return loop.run_until_complete(run())
