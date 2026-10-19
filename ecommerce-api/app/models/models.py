




from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import (
    Integer, String, Text, Numeric, DateTime, ForeignKey,
    UniqueConstraint, CheckConstraint, func, Enum as SQLEnum, Index, text, Boolean
)

from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.dialects.postgresql import ARRAY
import enum

from app.marketplace.enums import (
    ListingStatus, TrustLevel, VersionStatus,
    EvidenceType, EvidenceVisibility,
    OrderStatus, LedgerEntryType
)
class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    hashed_password: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[Optional[datetime]] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[Optional[datetime]] = mapped_column(Boolean, default=False, nullable=False)
    verification_code: Mapped[str] = mapped_column(Text, nullable=True)
    reset_code: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    roles: Mapped[List[str]] = mapped_column(ARRAY(string), server_default='{"buyer"}', nullable=False)

    __table_args__ = (
        CheckConstraint(
            "roles <@ ARRAY['buyer', 'seller', 'moderator', 'system']::varchar[]",
            name="check_valid_roles",
        ),
        Index=("idx_users_role_gin", "roles", postgresql_using="gin"),
    )

class RefreshToken(Base):
    __tablename__ = "refreshtokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[Optional[str]] = mapped_column(Text, nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(days=7)
    )
    is_revoked: Mapped[bool] = mapped_column(default=False)

class Prompt(Base):
    __tablename__ = "prompt"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    buyer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), on_delete="RESTRICT")
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"), on_delete="RESTRICT")
    version_id: Mapped[int] = mapped_column(ForeignKey("prompt_versions.id"), on_delete="RESTRICT")
    payment_intent_id: Mapped[int] = mapped_column(String(255), unique=True, nullable=True)
    purchase_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    platform_fee_rate: Mapped[Decimal] = mapped_column(Numeric(10, 4))
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(ListingStatus, native_enum=False, values_callable=lambda x: [e.value for e in x], create_constraint=True), default=OrderStatus.PENDING, server_default='pending')
    disputed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    verification_deadline: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
