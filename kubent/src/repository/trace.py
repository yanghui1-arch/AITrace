from typing import List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Trace

async def select_latest_traces_id_by_project_id(db: AsyncSession, project_id: int, counts: int = 3) -> List[UUID]:
    """Select latest traces id by project id.
    Default to search three traces.

    Args:
        db(AsyncSession): db conn
        project_id(int): project id
        counts(int): search counts
    
    Returns:
        A list of trace uuid
    """
    
    stmt = select(Trace.id).where(Trace.project_id == project_id).order_by(Trace.last_update_timestamp.desc()).limit(counts)
    result = await db.execute(stmt)
    return result.scalars().all()