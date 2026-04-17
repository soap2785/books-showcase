from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from .material import Material


class Audiobook(Material):
    __tablename__ = "audiobooks"

    type: Mapped[str] = mapped_column(String(20))

    __mapper_args__ = {
        "polymorphic_identity": "reader",
    }