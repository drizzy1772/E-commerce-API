
from fastapi import Query
from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")

class PaginationParams(BaseModel):
    offset: int = 0
    limit: int = 10

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    has_next: bool

