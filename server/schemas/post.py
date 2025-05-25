from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Post(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    author: str = Field(..., description = "The author of post")
    title: str = Field(..., description = "Title of the post")
    content: str = Field(..., description = "Content of the post")
    timestamp: datetime = Field(default_factory=datetime.now, description="Created at for post")
