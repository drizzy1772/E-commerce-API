



from datetime import datetime
from decimal import Decimal
from typing import List, Optional



from sqlalchemy import (
    Integer, String, Text, Numeric, DateTime, ForeignKey,
    ForeignKeyConstraint, UniqueConstraint, func, Enum as SQLEnum, CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship



from app.models.models import Base

from app.marketplace.enums import (
    ListingStatus, TrustLevel, VersionStatus,
    EvidenceType, EvidenceVisibility
)

class PromptListing(Base):
    __tablename__ = 'prompt_listings'

    id: Mapped[int] = mapped_column(primary_key=True)
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    current_version_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    title: Mapped[str] = mapped_column(String(255))

    public_description: Mapped[str] = mapped_column(Text)

    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    status: Mapped[ListingStatus] = mapped_column(SQLEnum(ListingStatus, native_enum=False, values_callable=lambda x: [e.value for e in x], create_constraint=True), default=ListingStatus.DRAFT, server_default='draft')
    trust_level: Mapped[TrustLevel] = mapped_column(SQLEnum(TrustLevel, native_enum=False, values_callable=lambda x: [e.value for e in x], create_constraint=True), default=TrustLevel.UNVERIFIED, server_default='unverified')

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        ForeignKeyConstraint(
            ["id", 'current_version_id'],
            ["prompt_versions.listing_id", "prompt_versions.id"],
            name="fk_listing_current_version",
            use_alter=True
        ),
        CheckConstraint('price > 0', name='check_price_positive')
    )

    versions: Mapped[List["PromptVersion"]] = relationship(
        back_populates='listing',
        foreign_keys="[PromptVersion.listing_id]"
    )

    current_version: Mapped[Optional["PromptVersion"]] = relationship(
        primaryjoin="and_(PromptListing.current_version_id == PromptVersion.id, PromptListing.id == PromptVersion.listing_id)",
        foreign_keys="[PromptListing.current_version_id]",
        post_update=True,
        overlaps="versions"
    )

class PromptVersion(Base):
    __tablename__ = "prompt_versions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    listing_id: Mapped[int] = mapped_column(Integer)

    version: Mapped[int] = mapped_column(Integer)

    prompt_text: Mapped[str] = mapped_column(Text)
    current_hash: Mapped[str] = mapped_column(String(64))
    
    status: Mapped[VersionStatus] = mapped_column(SQLEnum(VersionStatus, native_enum=False, values_callable=lambda x: [e.value for e in x], create_constraint=True), default=VersionStatus.DRAFT, server_default='draft')

    claimed_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), index=True, nullable=True)

    claimed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        ForeignKeyConstraint(
            ["listing_id"],
            ['prompt_listings.id'],
            name="fk_listing_id"
        ),
        UniqueConstraint(
            "listing_id",
            "version",
            name='uq_version_listing_id_version'
        ),
        UniqueConstraint(
            "listing_id",
            "id",
            name="uq_listing_id"
        ),
        CheckConstraint(
            'version >= 1', name='check_version_positive'
        )
    )

    listing: Mapped["PromptListing"] = relationship(back_populates="versions")
    evidence: Mapped[List["PromptEvidence"]] = relationship(back_populates="version")

class PromptEvidence(Base):
    __tablename__ = "prompt_evidence"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    version_id: Mapped[int] = mapped_column(Integer, ForeignKey("prompt_versions.id", ondelete="RESTRICT"), index=True)

    type: Mapped[EvidenceType] = mapped_column(SQLEnum(EvidenceType, native_enum=False, values_callable=lambda x: [e.value for e in x], create_constraint=True), default=EvidenceType.SCREENSHOT, server_default="screenshot")
    visibility: Mapped[EvidenceVisibility] = mapped_column(SQLEnum(EvidenceVisibility, native_enum=False, values_callable=lambda x: [e.value for e in x], create_constraint=True), default=EvidenceVisibility.MODERATOR_ONLY, server_default='moderator_only')

    model_used: Mapped[str] = mapped_column(String(255))

    storage_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    content_hash: Mapped[str] = mapped_column(String(64))
    prompt_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    caption: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    captured_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            '(storage_key IS NOT NULL AND url IS NULL) OR (storage_key IS NULL AND url IS NOT NULL)',
            name='check_storage_or_url'
        ),
        UniqueConstraint(
            'version_id', 'content_hash', name='uq_version_evidence_hash')
        )

    version: Mapped["PromptVersion"] = relationship(back_populates="evidence")
