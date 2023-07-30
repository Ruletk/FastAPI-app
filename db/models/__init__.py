from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    json_attributes = ()

    async def save(self, session: AsyncSession) -> None:
        """Saving the model."""
        session.add(self)
        await session.commit()

    async def delete(self, session: AsyncSession) -> None:
        """Light deletion. Change "is_active" to False"""
        self.is_active = False
        await self.save(session)

    async def full_delete(self, session: AsyncSession) -> None:
        """Full deletion, no mercy."""
        session.delete(self)
        await session.commit()

    async def update(self, session: AsyncSession, **attributes) -> None:
        """Updating the model. If attrubute did not exist, do nothing."""
        for key, value in attributes.items():
            setattr(self, key, value)
        await self.save(session)

    def jsonify(self) -> dict:
        """Jsonify the model. Json attrubutes will take from a tuple."""
        return {key: getattr(self, key, None) for key in self.json_attributes}


from . import user
