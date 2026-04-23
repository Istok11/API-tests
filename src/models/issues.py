from pydantic import BaseModel
from typing import Optional


class UsersResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    status: str
    author_id: int
    assignee_id: Optional[int] = None
    created_at: str
    updated_at: str