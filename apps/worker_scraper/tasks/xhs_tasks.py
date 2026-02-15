"""XHS keyword scrape task — search + upsert pipeline."""

import asyncio
from datetime import datetime
from typing import Any, Dict

from sqlalchemy.dialects.postgresql import insert as pg_insert

from apps.worker_scraper.celery_app import app
from libs.infra_db.session import AsyncSessionLocal
from plugins.platforms.xiaohongshu.adapter import XiaohongshuAdapter
from plugins.platforms.xiaohongshu.models import XhsNote
from plugins.platforms.xiaohongshu.config import XhsConfig
from libs.core_kernel.interfaces.platform import PlatformCredentials
from libs.core_kernel.plugin_loader import PluginManager

import structlog

logger = structlog.get_logger()


@app.task(bind=True, max_retries=2, default_retry_delay=10)
def scrape_xhs_keyword_task(
    self, tenant_id: str, keyword: str, sort_type: str = "general"
) -> Dict[str, Any]:
    """Scrape XHS search results for a keyword and upsert into DB.

    Returns:
        {"saved": int, "keyword": str}
    """

    async def run() -> Dict[str, Any]:
        logger.info(
            "xhs_scrape_start",
            tenant_id=tenant_id,
            keyword=keyword,
            sort=sort_type,
        )

        # 1. Initialize adapter & login
        adapter = XiaohongshuAdapter(tenant_id=tenant_id)

        # Load XHS config for this tenant (cookie, proxy)
        # For now, use env-based or default config
        config = XhsConfig.load(tenant_id=tenant_id)
        creds = PlatformCredentials(
            cookies={"web_session": config.cookie},
            proxy_url=config.proxy_url,
        )
        await adapter.login(creds)

        # 2. Search
        raw_notes = await adapter.search_notes(
            keyword=keyword, sort=sort_type, page=1, page_size=20
        )

        if not raw_notes:
            logger.warn("xhs_scrape_empty", keyword=keyword)
            return {"saved": 0, "keyword": keyword}

        # 3. Upsert into Postgres
        now = datetime.utcnow()
        saved = 0

        async with AsyncSessionLocal() as session:
            for note in raw_notes:
                stmt = pg_insert(XhsNote).values(
                    note_id=note["note_id"],
                    title=note["title"],
                    desc=note.get("desc", ""),
                    cover_url=note.get("cover_url", ""),
                    likes=note.get("likes", 0),
                    comments=note.get("comments", 0),
                    collects=note.get("collects", 0),
                    user_nickname=note.get("user_nickname", ""),
                    user_id=note.get("user_id", ""),
                    keyword_search=keyword,
                    last_scraped_at=now,
                    tenant_id=tenant_id,
                )

                # ON CONFLICT — update engagement metrics + timestamp
                stmt = stmt.on_conflict_do_update(
                    index_elements=["note_id"],
                    set_={
                        "likes": stmt.excluded.likes,
                        "comments": stmt.excluded.comments,
                        "collects": stmt.excluded.collects,
                        "last_scraped_at": stmt.excluded.last_scraped_at,
                        "keyword_search": stmt.excluded.keyword_search,
                    },
                )

                await session.execute(stmt)
                saved += 1

            await session.commit()

        logger.info("xhs_scrape_done", keyword=keyword, saved=saved)
        return {"saved": saved, "keyword": keyword}

    # Run async code in sync Celery task
    try:
        return asyncio.run(run())
    except Exception as exc:
        logger.error("xhs_scrape_failed", error=str(exc), keyword=keyword)
        raise self.retry(exc=exc)
