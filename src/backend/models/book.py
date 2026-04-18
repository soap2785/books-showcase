from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer

from .material import Material


class Book(Material):
    __tablename__ = "books"

    pages: Mapped[int] = mapped_column(Integer)

    type: Mapped[str] = mapped_column(String(20))

    __mapper_args__ = {
        "polymorphic_identity": "reader",
    }