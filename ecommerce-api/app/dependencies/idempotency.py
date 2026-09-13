
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.models.idempotency import IdempotencyKey
from app.models.enums import IdempotencyStatus
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError


async def check_idempotency_key(
        idempotency_key: str | None = Header(default=None),
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    if idempotency_key is None:
        raise HTTPException(status_code=400, detail="Header is None")

    stmt = select(IdempotencyKey).where(IdempotencyKey.key == idempotency_key,
                              IdempotencyKey.user_id == current_user.id)
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing is not None and existing.status == IdempotencyStatus.COMPLETED:
        return JSONResponse(content=existing.response_body, status_code=existing.response_status)

    if existing is not None and existing.status == IdempotencyStatus.PROCESSING:
        raise HTTPException(status_code=409, detail="existing")

    new_record = IdempotencyKey(
        key=idempotency_key,
        user_id=current_user.id,
        status=IdempotencyStatus.PROCESSING
    )

    try:
        db.add(new_record)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="existing")
