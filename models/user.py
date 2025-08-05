from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from sqlalchemy import String, Integer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.task import TaskOrm


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=True)
    # # связь 1-n
    tasks: Mapped[list["TaskOrm"]] = relationship(
        "TaskOrm", back_populates="user", cascade="all, delete-orphan"
    )
