from pydantic import BaseModel
from datetime import datetime

class MatchBase(BaseModel):
    name: str
    created_by_id: int

class MatchCreate(MatchBase):
    pass

class Match(MatchBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True