from typing import Union
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.user import User


class UserDAL:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create_user(self, nickname: str, email: str) -> User:
        new_user = User(nickname=nickname, email=email)
        await new_user.save(self.db_session)
        return new_user

    async def delete_user(self, user_id: UUID) -> Union[User, None]:
        user = await self.get_user_by_id(user_id)
        if user is not None and user.is_active:
            await user.delete(self.db_session)
            return user

    async def update_user(self, user_id: UUID, **kwargs) -> Union[UUID, None]:
        user = await self.get_user_by_id(user_id)
        await user.update(self.db_session, **kwargs)
        if user is not None:
            return user

    # Get functions
    async def get_user_by_id(self, user_id: UUID) -> Union[User, None]:
        stmt = select(User).where(User.user_id == user_id)
        return await self._get_user(stmt)

    async def get_user_by_nickname(self, nickname: str) -> Union[User, None]:
        stmt = select(User).where(User.nickname == nickname)
        return await self._get_user(stmt)

    async def get_user_by_email(self, email: str) -> Union[User, None]:
        stmt = select(User).where(User.email == email)
        return await self._get_user(stmt)

    async def _get_user(self, stmt) -> Union[UUID, None]:
        user = await self.db_session.scalar(stmt)
        if user is not None:
            return user

    # -------------
