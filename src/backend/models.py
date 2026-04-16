from typing import Optional
from enum import StrEnum

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, TypeDecorator, Float, CheckConstraint, ForeignKey, Boolean
from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash, check_password_hash

from config import CRYPTO_KEY

cipher = Fernet(CRYPTO_KEY)


class ReaderAction(StrEnum):
    READED = "readed"
    LISTENED = "listened"
    FAVOURITE = "favourite"
    WANTED = "wanted"
    BOUGHT = "bought"


class EncryptedString(TypeDecorator):
    """Тип данных, который шифрует строку перед сохранением в БД."""
    impl = String

    def process_bind_param(self, value, dialect):
        if value is not None:
            return cipher.encrypt(value.encode()).decode()
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return cipher.decrypt(value.encode()).decode()
        return value


class Base(DeclarativeBase):
    pass


class ReaderAssociation(Base):
    __tablename__ = "reader_associations"

    reader_id: Mapped[int] = mapped_column(ForeignKey("readers.id"), primary_key=True)
    item_id: Mapped[int] = mapped_column(primary_key=True)
    item_type: Mapped[str] = mapped_column(String(20), primary_key=True)
    action_type: Mapped[ReaderAction] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(EncryptedString(320))
    _password_hash: Mapped[str] = mapped_column(String(255))

    type: Mapped[str] = mapped_column(String(20))

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "user",
    }

    @property
    def password(self):
        raise AttributeError("Пароль нельзя прочитать напрямую")

    @password.setter
    def password(self, password):
        self._password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self._password_hash, password)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, type={self.type!r})"


class Reader(User):
    __tablename__ = "readers"

    actions: Mapped[list["ReaderAssociation"]] = relationship(cascade="all, delete-orphan")

    type: Mapped[str] = mapped_column(String(20))

    __mapper_args__ = {
        "polymorphic_identity": "reader",
    }


class Author(User):
    __tablename__ = "authors"

    published_books: Mapped[list["Book"]] = relationship(back_populates="author_rel")
    rating: Mapped[float] = mapped_column(
        Float, 
        CheckConstraint("rating >= 0 AND rating <= 5"), 
        default=0.0
    )

    type: Mapped[str] = mapped_column(String(20))

    __mapper_args__ = {
        "polymorphic_identity": "author",
    }


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    rating: Mapped[float] = mapped_column(
        Float, 
        CheckConstraint("rating >= 0 AND rating <= 5"), 
        default=0.0
    )
    genre: Mapped[str] = mapped_column(String(30))
    is_mature_content: Mapped[bool] = mapped_column(Boolean, default=False)


class Audiobook(Base):
    __tablename__ = "audiobooks"

    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    rating: Mapped[float] = mapped_column(
        Float, 
        CheckConstraint("rating >= 0 AND rating <= 5"), 
        default=0.0
    )
    is_mature_content: Mapped[bool] = mapped_column(Boolean, default=False)
    audio: Mapped[str] = mapped_column(String(50))


class Feedback(Base):
    __tablename__ = "feedbacks"

    id: Mapped[int] = mapped_column(primary_key=True)
    reader: Mapped[int] = mapped_column(ForeignKey("readers.id"))
    author: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    book: Mapped[Optional[int]] = mapped_column(ForeignKey("books.id"))
    audiobook: Mapped[Optional[int]] = mapped_column(ForeignKey("audiobooks.id"))
    rating: Mapped[float] = mapped_column(
        Float, 
        CheckConstraint("rating >= 0 AND rating <= 5"), 
        default=0.0
    )
    comment: Mapped[Optional[str]] = mapped_column(String(500))
