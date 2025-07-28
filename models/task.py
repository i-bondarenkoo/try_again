from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base
from uuid import UUID
from sqlalchemy import String, DateTime
from datetime import datetime
import uuid
from datetime import datetime


class TaskOrm(Base):
    __tablename__ = "tasks"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(50), nullable=False)
    # имя сотрудника
    assignee: Mapped[str] = mapped_column(String(35), nullable=False)
    status: Mapped[str] = mapped_column(String(35), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
