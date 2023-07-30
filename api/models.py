import re
import uuid

from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator, constr


LETTER_MATCH_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_-]+$")


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
        if len(value) > 120:
            raise HTTPException(status_code=422, detail="Nickname should ")
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422,
                detail="Nickname should start with a letter and contain only letters, numbers and underscores",
            )
        return value


class DeleteUserResponse(BaseModel):
    deleted_user_id: uuid.UUID


class UpdatedUserResponse(BaseModel):
    updated_user_id: uuid.UUID


class UpdateUserRequest(BaseModel):
    nickname: Optional[constr(min_length=1)]
    email: Optional[EmailStr]

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
