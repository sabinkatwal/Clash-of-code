from pydantic import BaseModel
from datetime import datetime

class SubmissionBase(BaseModel):
    user_id: int
    match_id: int
    code: str

class SubmissionCreate(SubmissionBase):
    pass

class Submission(SubmissionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True