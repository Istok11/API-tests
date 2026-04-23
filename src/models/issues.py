
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

#GET ISSUES, READ ISSUES
class IssueResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    status: str
    author_id: int
    assignee_id: Optional[int] = None
    created_at: str
    updated_at: str

#CREATE ISSUES, EDIT ISSUES
class CreateIssueRequest(BaseModel):
    title: str
    description: str
    priority: str
    assignee_id: Optional[int] = None





# EDIT ISSUE
class EditIssueRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    assignee_id: Optional[int] = None





# DELETE ISSUE
class DeleteIssueResponse(BaseModel):
    ok: bool


# META STATUSES
class Status(str, Enum):
    open = "open"
    in_progress = "in_progress"
    ready_for_qa = "ready_for_qa"
    qa = "qa"
    done = "done"
    closed = "closed"

class MetaStatusesForQaResponse(BaseModel):
    all_statuses: list[Status]
    allowed_statuses: list[Status]



# CHANGE STATUS OF ISSUE
class ChangeStatusIssueRequest(BaseModel):
    new_status: str

