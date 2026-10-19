




from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import (
    Integer, String, Text, Numeric, DateTime, ForeignKey,
    UniqueConstraint, CheckConstraint, func, Enum as SQLEnum, Index, text, Boolean
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.dialects.postgresql import ARRAY

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

    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    verification_code: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    reset_code: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    roles: Mapped[List[str]] = mapped_column(ARRAY(String), server_default='{"buyer"}', nullable=False)

    __table_args__ = (
        CheckConstraint(
            "roles <@ ARRAY['buyer', 'seller', 'moderator', 'system']::varchar[]",
            name="check_valid_roles",
        ),
        Index("idx_users_role_gin", "roles", postgresql_using="gin"),
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

class PromptOrder(Base):
    __tablename__ = "prompt_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    buyer_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), index=True)
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), index=True)

    version_id: Mapped[int] = mapped_column(ForeignKey("prompt_versions.id", ondelete="RESTRICT"))
    
    payment_intent_id: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)
    
    purchase_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    platform_fee_rate: Mapped[Decimal] = mapped_column(Numeric(10, 4))
    
    status: Mapped[OrderStatus] = mapped_column(
        SQLEnum(OrderStatus, native_enum=False, values_callable=lambda x: [e.value for e in x], create_constraint=True),
        default=OrderStatus.PENDING,
        server_default='pending'
    )

    buyer_confirmed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    disputed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    verification_deadline: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    __table_args__ = (
        CheckConstraint("purchase_price > 0", name="check_purchase_price_positive"),
        CheckConstraint("platform_fee_rate >= 0 AND platform_fee_rate < 1", name="check_fee_rate_bounds"),
        Index(
            "idx_unique_active_purchase",
            "buyer_id",
            "version_id",
            unique=True,
            postgresql_where=text("status NOT IN ('abandoned', 'payment_failed', 'refunded')")
        )
    )

class PromptLedgerEntry(Base):
    __tablename__ = "prompt_ledger_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), index=True)

    order_id: Mapped[int] = mapped_column(ForeignKey("prompt_orders.id", ondelete="RESTRICT"), index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    entry_type: Mapped[LedgerEntryType] = mapped_column(
        SQLEnum(LedgerEntryType, native_enum=False, values_callable=lambda x: [e.value for e in x], create_constraint=True)
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint('amount > 0', name="check_amount_positive"),
        UniqueConstraint('order_id', 'entry_type', name="uq_order_entry_type")
    )

class ModerationReview(Base):
    __tablename__ = "moderation_reviews"
    id: Mapped[int] = mapped_column(primary_key=True)

    version_id: Mapped[int] = mapped_column(ForeignKey("prompt_versions.id", ondelete="RESTRICT"), index=True)
    moderator_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), index=True)

    decision: Mapped[str] = mapped_column(String(50))
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class OrderFeedback(Base):
    __tablename__ = "order_feedback"

    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(ForeignKey("prompt_orders.id", ondelete="RESTRICT"), unique=True)
    notes: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class DisputeEvidence(Base):
    __tablename__ = "dispute_evidence"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("prompt_orders.id", ondelete="RESTRICT"), index=True)
    
    type: Mapped[EvidenceType] = mapped_column(
        SQLEnum(EvidenceType, native_enum=False, values_callable=lambda x: [e.value for e in x], create_constraint=True)
    )

    storage_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    caption: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint(
        "(storage_key IS NOT NULL and url IS NULL) OR (storage_key IS NULL and url IS NOT NULL)",
         name="check_dispute_storage_or_url"
        ),         
    )


class StatusEvent(Base):
    __tablename__ = "status_events"

    id: Mapped[int] = mapped_column(primary_key=True)

    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[int] = mapped_column(Integer, nullable=False)
    
    from_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    to_status: Mapped[str] = mapped_column(String(50), nullable=False)
    
    actor_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("idx_status_event_entity", "entity_type", "entity_id"),
    )