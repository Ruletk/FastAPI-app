import uuid

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID

from . import BaseModel


class User(BaseModel):
    __tablename__ = "users"
    json_attributes = ("user_id", "username", "nickname", "email", "is_active")

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nickname = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    is_active = Column(Boolean, default=True)
