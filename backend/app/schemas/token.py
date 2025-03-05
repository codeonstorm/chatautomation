from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: str
    exp: int
    type: str

class RefreshToken(BaseModel):
    refresh_token: str

