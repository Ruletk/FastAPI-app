from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    json_attributes = ()

    def save(self, session: AsyncSession) -> None:
        """Saving the model."""
        session.add(self)
        session.commit()

    def delete(self, session: AsyncSession) -> None:
        """Light deletion. Change "is_active" to False"""
        self.is_active = False
        self.save(session)

    def full_delete(self, session: AsyncSession) -> None:
        """Full deletion, no mercy."""
        session.delete(self)
        session.commit()

    def update(self, **attributes) -> None:
        """Updating the model. If attrubute did not exist, do nothing."""
        (setattr(self, key, value) for key, value in attributes.items())
        self.save()

    def jsonify(self) -> dict:
        """Jsonify the model. Json attrubutes will take from a tuple."""
        return {key: getattr(self, key, None) for key in self.json_attributes}


from . import user
