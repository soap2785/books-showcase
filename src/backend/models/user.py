from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from werkzeug.security import generate_password_hash, check_password_hash

from .base import Base
from .custom_types import EncryptedString


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
