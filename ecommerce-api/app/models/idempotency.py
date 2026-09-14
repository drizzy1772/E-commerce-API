


from app.models.enums import IdempotencyStatus
from datetime import datetime, timezone, timedelta
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import JSON, JSONB
from app.models.models import Base


class IdempotencyKey(Base):
    __tablename__ = "idempotencykey"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    response_status: Mapped[int] = mapped_column(Integer, nullable=True)
    response_body: Mapped[dict] = mapped_column(JSON, nullable=True)
    status: Mapped[IdempotencyStatus] = mapped_column(
        Enum(IdempotencyStatus, name="idempotency_status"),
        default=IdempotencyStatus.PROCESSING
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(minutes=30),
        nullable=False
    )