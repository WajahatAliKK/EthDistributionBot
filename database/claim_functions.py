import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Claims

async def claimed(user_id, db):
    async with db() as session:
        claim = await session.execute(
            db.query(Claims).filter(Claims.user_id == user_id).first()
        )
        if claim:
            return claim.scalar().claimed
        return False

async def add_claim(user_id, claim_data, db):
    async with db() as session:
        claim = Claims(**claim_data, user_id=user_id)
        session.add(claim)
        await session.commit()
        await session.refresh(claim)
        return claim

async def change_state(user_id, db):
    async with db() as session:
        claim = await session.execute(
            db.query(Claims).filter(Claims.user_id == user_id).first()
        )
        if claim:
            claim = claim.scalar()
            claim.claimed = not claim.claimed
            await session.commit()
            await session.refresh(claim)
            return claim
        return None
