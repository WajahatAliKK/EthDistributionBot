import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import Claims

async def claimed(user_id, db):
    async with db.AsyncSession() as session:
        claim = await session.execute(
            select(Claims).filter(Claims.user_id == user_id)
        )
        if claim:
            return claim.scalar_one_or_none()
        return False

async def add_claim(user_id, claim_data, db):
    async with db.AsyncSession() as session:
        claim = Claims(**claim_data, user_id=user_id)
        session.add(claim)
        await session.commit()
        await session.refresh(claim)
        return claim

async def change_state(user_id, db):
    async with db.AsyncSession() as session:
        claim = await session.execute(
            select(Claims).filter(Claims.user_id == user_id).first()
        )
        if claim:
            claim = claim.scalar()
            claim.claimed = not claim.claimed
            await session.commit()
            await session.refresh(claim)
            return claim
        return None
