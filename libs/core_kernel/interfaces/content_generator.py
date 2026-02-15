from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class GenerationContext(BaseModel):
    platform: str
    topic: str
    keywords: List[str] = Field(default_factory=list)
    tone: Optional[str] = "professional"
    max_length: int = 500

class GeneratedContent(BaseModel):
    title: str
    body: str
    hashtags: List[str] = Field(default_factory=list)
    suggested_media_prompts: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class IContentGenerator(ABC):
    """
    Interface for AI Content Generation services (e.g., GPT-4, Claude, Local LLM).
    """
    
    @abstractmethod
    async def generate(self, prompt: str, context: GenerationContext) -> GeneratedContent:
        """Generate content based on prompt and context."""
        pass
