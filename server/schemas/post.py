from datetime import datetime

from pydantic import BaseModel, Field


class Post(BaseModel):
    user_id: int = Field(..., description="Owner post ID")
    content: str = Field(..., description="Content of the post")
    timestamp: datetime = Field(default_factory=datetime.now, description="Created at for post")
