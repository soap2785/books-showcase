from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Float, CheckConstraint, String, ForeignKey

from .base import Base
from .reader import Reader


class Feedback(Base):
    __tablename__ = "feedbacks"

    id: Mapped[int] = mapped_column(primary_key=True)
    reader_rel: Mapped["Reader"] = relationship(back_populates="comments")
    author: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    book: Mapped[Optional[int]] = mapped_column(ForeignKey("books.id"))
    audiobook: Mapped[Optional[int]] = mapped_column(ForeignKey("audiobooks.id"))
    rating: Mapped[float] = mapped_column(
        Float, CheckConstraint("rating >= 0 AND rating <= 5"), default=0.0
    )
    comment: Mapped[Optional[str]] = mapped_column(String(500))
