from typing import Dict, List, Any
from uuid import UUID
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from .base import Base

class Step(Base):
    __tablename__ = "step"
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    trace_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    parent_step_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    type: Mapped[str] = mapped_column(String(255), nullable=False)
    tags: Mapped[List[str]] = mapped_column(JSONB, nullable=False)
    input: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    output: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    error_info: Mapped[str | None] = mapped_column(String(255), nullable=True)
    model: Mapped[str | None] = mapped_column(String(255), nullable=True)
    project_name: Mapped[str] = mapped_column(String(255), nullable=False)
    usage: Mapped[Dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, nullable=False)
