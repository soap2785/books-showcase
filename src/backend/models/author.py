from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, CheckConstraint

from .user import User
from .book import Book
from .audiobook import Audiobook


class Author(User):
    __tablename__ = "authors"

    published_books: Mapped[list["Book"]] = relationship(back_populates="author_rel")
    published_audiobboks: Mapped[list["Audiobook"]] = relationship(back_populates="author_rel")
    rating: Mapped[float] = mapped_column(
        Float, 
        CheckConstraint("rating >= 0 AND rating <= 5"), 
        default=0.0
    )

    type: Mapped[str] = mapped_column(String(20))

    __mapper_args__ = {
        "polymorphic_identity": "author",
    }