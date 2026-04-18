from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from .base import Base
from .user import User
from enums import ReaderAction


class ReaderAssociation(Base):
    __tablename__ = "reader_associations"

    reader_id: Mapped[int] = mapped_column(ForeignKey("readers.id"), primary_key=True)
    item_id: Mapped[int] = mapped_column(primary_key=True)
    item_type: Mapped[str] = mapped_column(String(20), primary_key=True)
    action_type: Mapped[ReaderAction] = mapped_column(primary_key=True)


class Reader(User):
    __tablename__ = "readers"

    actions: Mapped[list["ReaderAssociation"]] = relationship(
        cascade="all, delete-orphan"
    )

    type: Mapped[str] = mapped_column(String(20))

    __mapper_args__ = {
        "polymorphic_identity": "reader",
    }
