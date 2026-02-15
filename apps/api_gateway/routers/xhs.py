from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from datetime import datetime

from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from plugins.platforms.xiaohongshu.config import XhsConfig
from plugins.platforms.xiaohongshu.adapter import XiaohongshuAdapter
from plugins.platforms.xiaohongshu.models import XhsNote
from libs.core_kernel.interfaces.platform import PlatformCredentials
from libs.infra_db.session import get_db_session

router = APIRouter(prefix="/xhs", tags=["Xiaohongshu Plugin"])

# --- Request / Response Models ---

class TestConfigRequest(BaseModel):
    config: XhsConfig
    tenant_id: str = "default"

class TestConfigResponse(BaseModel):
    success: bool
    message: str
    metadata: Dict[str, Any]

class ScrapeRequest(BaseModel):
    keyword: str
    sort_type: str = "general"  # general | time_descending | popularity_descending

class ScrapeResponse(BaseModel):
    task_id: str
    message: str

class NoteOut(BaseModel):
    note_id: str
    title: str
    desc: str
    cover_url: str
    likes: int
    comments: int
    collects: int
    user_nickname: str
    user_id: str
    keyword_search: str
    last_scraped_at: datetime
    tenant_id: str

class PaginatedNotes(BaseModel):
    items: List[NoteOut]
    total: int
    page: int
    page_size: int


# --- Endpoints ---

@router.post("/test-config", response_model=TestConfigResponse)
async def test_xhs_config(payload: TestConfigRequest):
    """
    Test a Xiaohongshu configuration by attempting to fetch the user profile.
    This does NOT save the config, just validates the cookie.
    """
    try:
        adapter = XiaohongshuAdapter(tenant_id=payload.tenant_id)
        creds = PlatformCredentials(
            cookies={"web_session": payload.config.cookie},
            proxy_url=payload.config.proxy_url
        )
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


@router.post("/scrape", response_model=ScrapeResponse)
async def trigger_scrape(payload: ScrapeRequest):
    """Trigger an async Celery task to scrape XHS keyword search results."""
    from apps.worker_scraper.tasks.xhs_tasks import scrape_xhs_keyword_task

    # TODO: Extract tenant_id from auth middleware / JWT
    tenant_id = "default"

    task = scrape_xhs_keyword_task.delay(
        tenant_id=tenant_id,
        keyword=payload.keyword,
        sort_type=payload.sort_type,
    )

    return ScrapeResponse(
        task_id=task.id,
        message=f"采集任务已启动: {payload.keyword}",
    )


@router.get("/notes", response_model=PaginatedNotes)
async def list_notes(
    keyword: Optional[str] = Query(None, description="Filter by search keyword"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db_session),
):
    """Return paginated XhsNote list for the current tenant."""
    # TODO: Extract tenant_id from auth middleware
    tenant_id = "default"

    # Base query
    base = select(XhsNote).where(XhsNote.tenant_id == tenant_id)
    count_q = select(func.count()).select_from(XhsNote).where(XhsNote.tenant_id == tenant_id)

    if keyword:
        base = base.where(XhsNote.keyword_search == keyword)
        count_q = count_q.where(XhsNote.keyword_search == keyword)

    # Count
    total_result = await db.execute(count_q)
    total = total_result.scalar() or 0

    # Fetch page
    stmt = (
        base
        .order_by(desc(XhsNote.last_scraped_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    notes = result.scalars().all()

    return PaginatedNotes(
        items=[NoteOut.model_validate(n, from_attributes=True) for n in notes],
        total=total,
        page=page,
        page_size=page_size,
    )
