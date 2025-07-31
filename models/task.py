from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy import String, DateTime
from datetime import datetime
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.user import UserOrm


class TaskOrm(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(String(35), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )

    user: Mapped["UserOrm"] = relationship("UserOrm", back_populates="tasks")
