


import enum

class IdempotencyStatus(str, enum.Enum):
    PROCESSING = "processing"
    COMPLETED = "completed"