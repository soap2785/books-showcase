from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from .material import Material


class Book(Material):
    __tablename__ = "books"

    type: Mapped[str] = mapped_column(String(20))

    __mapper_args__ = {
        "polymorphic_identity": "reader",
    }