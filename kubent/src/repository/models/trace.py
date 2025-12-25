from typing import Dict, List, Any
from uuid import UUID
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from .base import Base

class Trace(Base):
    __tablename__ = "trace"
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    project_name: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    conversation_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    tags: Mapped[List[str]] = mapped_column(JSONB, nullable=False)
    input: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    output: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    error_info: Mapped[str | None] = mapped_column(String(255), nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    last_update_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, nullable=False)
