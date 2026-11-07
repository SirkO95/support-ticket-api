from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class CommentCreate(BaseModel):
    author: str
    content: str

class CommentOut(BaseModel):
    id: int
    author: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class TicketCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: str
    priority: str = "medium"

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None

class TicketOut(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime
    comments: List[CommentOut] = []

    class Config:
        from_attributes = True