from pydantic import BaseModel



class UsersResponse(BaseModel):
    id: int
    email: str
    role: str
    created_at: str