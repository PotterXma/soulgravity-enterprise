from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# --- Scraping Models ---

class ScrapedNote(BaseModel):
    """
    Represents a raw note scraped from Xiaohongshu search results.
    """
    note_id: str
    title: str
    type: str = "normal"  # normal, video
    user_id: str
    user_nickname: str
    user_avatar: str
    likes: int = 0
    comments: int = 0
    collected: int = 0  # saves
    shared: int = 0
    cover_url: str
    note_url: str
    scraped_at: datetime = Field(default_factory=datetime.utcnow)

class SearchParams(BaseModel):
    keyword: str
    sort: Literal["general", "time_descending", "popularity_descending"] = "general"
    page: int = 1
    page_size: int = 20

# --- Publishing Models ---

class ImageUploadResult(BaseModel):
    file_id: str
    url: Optional[str] = None
    width: int
    height: int

class PublishRequest(BaseModel):
    """
    Payload for creating a new note.
    """
    title: str = Field(..., max_length=20)
    content: str = Field(..., max_length=1000)
    image_ids: List[str] = Field(..., description="List of file_ids from upload step", min_length=1)
    topics: List[str] = Field(default_factory=list, description="List of hashtags/topics")
    is_private: bool = False
    post_time: Optional[str] = None  # YYYY-MM-DD HH:mm:ss if scheduled

class PublishResponse(BaseModel):
    note_id: str
    link: str
    raw_response: Dict[str, Any]
