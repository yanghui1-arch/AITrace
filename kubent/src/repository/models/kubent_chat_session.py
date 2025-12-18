from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, Integer, Text, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from .base import Base

class KubentChatSession(Base):
    __tablename__ = "kubent_chat_session"
    
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_uuid: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    topic: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    last_update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), 
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"), 
        onupdate=text("CURRENT_TIMESTAMP")
    )
    total_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)