from pydantic import BaseModel


# REGISTER
class RegisterRequest(BaseModel):
    email: str
    password: str
    role: str


class RegisterResponse(BaseModel):
    id: int
    email: str
    role: str
    created_at: str

# AUTH

class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
