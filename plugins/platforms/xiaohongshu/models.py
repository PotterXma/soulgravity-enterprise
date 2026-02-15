"""XhsNote — Persisted Xiaohongshu note for keyword search results."""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class XhsNote(SQLModel, table=True):
    """A scraped Xiaohongshu note, keyed by note_id for upsert deduplication."""

    __tablename__ = "xhs_note"

    note_id: str = Field(primary_key=True, max_length=64, description="XHS unique note ID")
    title: str = Field(default="", max_length=512)
    desc: str = Field(default="", sa_type_kwargs={"length": None})  # TEXT
    cover_url: str = Field(default="", max_length=1024)

    # Engagement metrics (updated on each scrape)
    likes: int = Field(default=0)
    comments: int = Field(default=0)
    collects: int = Field(default=0)

    # Author
    user_nickname: str = Field(default="", max_length=128)
    user_id: str = Field(default="", max_length=64)

    # Search context
    keyword_search: str = Field(default="", max_length=256, description="Keyword that found this note")

    # Timestamps
    last_scraped_at: datetime = Field(default_factory=datetime.utcnow)

    # Multi-tenancy
    tenant_id: str = Field(default="default", max_length=64, index=True)
