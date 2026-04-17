from sqlalchemy import String, TypeDecorator
from cryptography.fernet import Fernet

from config import CRYPTO_KEY

cipher = Fernet(CRYPTO_KEY)


class EncryptedString(TypeDecorator):
    """Type that encryptes data before commit."""
    impl = String

    def process_bind_param(self, value, dialect):
        if value is not None:
            return cipher.encrypt(value.encode()).decode()
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return cipher.decrypt(value.encode()).decode()
        return value