from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User


class UserDAL:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create_user(self, nickname: str, email: str) -> User:
        new_user = User(nickname=nickname, email=email)
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user
