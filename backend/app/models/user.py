from sqlalchemy.orm import Mapped, mapped_column

from . import Base
from .mixins import TimestampMixin, UUIDMixin


class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(index=True, max_length=50, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(max_length=100, nullable=False)
    first_name: Mapped[str] = mapped_column(max_length=50, nullable=False)
    last_name: Mapped[str] = mapped_column(max_length=50, nullable=False)

    @property
    def full_name(self) -> str:
        return self.first_name + self.last_name
