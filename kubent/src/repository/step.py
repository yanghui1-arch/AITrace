from typing import List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Step

async def select_steps_by_trace_id(db: AsyncSession, trace_id: UUID) -> List[Step]:
    stmt = select(Step).where(Step.trace_id == trace_id)
    result = await db.execute(stmt)
    return result.scalars().all()
