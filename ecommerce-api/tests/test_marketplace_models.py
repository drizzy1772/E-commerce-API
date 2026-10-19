

from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import (
    Integer, String, Text, Numeric, DateTime, ForeignKey,
    ForeignKeyConstraint, UniqueConstraint, CheckConstraint, 
    func, Enum as SQLEnum, Index, text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY

from app.core.database import Base
from app.marketplace.enums import (
    ListingStatus, TrustLevel, VersionStatus,
    EvidenceType, EvidenceVisibility,
    OrderStatus, LedgerEntryType
)


class PromptOrder(Base):
    __tablename__ = "prompt_orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    buyer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    version_id: Mapped[int] = mapped_column(ForeignKey("prompt_versions.id"), index=True)

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
        CheckConstraint("purchase_price > 0", name="check_purchase_paid_positive"),
        Index(
            "idx_unique_active_purchase",
            "buyer_id",
            "version_id",
            unique=True,
            postgresql_where=text("status NOT IN ('abandoned', 'payment_failed', 'refunded')")
        )
    )




class LedgerEntry(Base):
    __tablename__ = "prompt_ledger_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("prompt_orders.id"), index=True)

    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    entry_type: Mapped[LedgerEntryType] = mapped_column(
        SQLEnum(LedgerEntryType, native_enum=False, values_callable=lambda x: [e.value for e in x], create_constraint=True)
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint('amount > 0', name="check_amount_positive"),
        UniqueConstraint('order_id', 'entry_type', name='uq_order_entry_type'),
    )
    