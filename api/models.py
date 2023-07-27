import re
import uuid

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator


LETTER_MATCH_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9]+$")


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class ShowUser(TunedModel):
    user_id: uuid.UUID
    nickname: str
    email: EmailStr
    is_active: bool


class UserCreate(BaseModel):
    nickname: str
    email: EmailStr

    @validator("nickname")
    def validate_name(cls, value):
        if len(value) <= 3:
            raise HTTPException(
                status_code=422, detail="Nickname should contain 3 or more characters"
            )
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Nickname should contain only letters"
            )
        return value


class DeleteUserResponse(TunedModel):
    deleted_user_id: uuid.UUID
