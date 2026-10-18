







from enum import Enum


class ListingStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    WITHDRAWN = "withdrawn"

class TrustLevel(str, Enum):
    UNVERIFIED = "unverified"
    MODERATED = "moderated"
    COMMUNITY_VERIFIED = "community_verified"

class VersionStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    IN_REVIEW = "in_review"
    CHANGES_REQUESTED = "changes_requested"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"

class EvidenceType(str, Enum):
    SCREENSHOT = "screenshot"
    CHAT_LOG = "chat_log"
    LINK = "link"

class EvidenceVisibility(str, Enum):
    PUBLIC = "public"
    MODERATOR_ONLY = "moderator_only"

class OrderStatus(str, Enum):
    PENDING = "pending"
    PAYMENT_FAILED = "payment_failed"
    PAID_HELD = "paid_held"
    DELIVERED = "delivered"
    DELIVERY_FAILED = "delivery_failed"
    DISPUTED = "disputed"
    ESCALATED = "escalated"
    RELEASED = "released"
    REFUNDED = "refunded"
    ABANDONED = "abandoned"

class LedgerEntryType(str, Enum):
    SELLER_PAYOUT = "seller_payout"
    PLATFORM_FEE = "platform_fee"
    BUYER_REFUND = "buyer_refund"
