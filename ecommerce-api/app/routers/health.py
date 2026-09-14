

from sqlalchemy import text
from fastapi import FastAPI, HTTPException, status, APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.get("/ready")
async def readiness_check(request: Request, db: Session = Depends(get_db)):

    try:
        await db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    try:
        await request.app.state.redis.ping()
        redis_ok = True
    except Exception:
        redis_ok = False

    if not db_ok or not redis_ok:
        raise HTTPException(status_code=503, detail="service unavailable")

    return {"status": "ready"}