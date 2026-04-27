from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Float, CheckConstraint, String, Boolean

from .base import Base
from .author import Author


class Material(Base):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_rel: Mapped["Author"] = relationship(back_populates="published_books")
    rating: Mapped[float] = mapped_column(
        Float, CheckConstraint("rating >= 0 AND rating <= 5"), default=0.0
    )
    title: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(700))
    genre: Mapped[str] = mapped_column(String(30))
    is_mature_content: Mapped[bool] = mapped_column(Boolean, default=False)
    file: Mapped[str] = mapped_column(String(30))
