from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class OrderCreate(BaseModel):
    ticket_type_id: UUID
    quantity: int = Field(ge=1, le=10)


class OrderResponse(BaseModel):
    id: UUID
    user_id: UUID
    ticket_type_id: UUID
    quantity: int = Field(ge=1, le=10)
    unit_price: float
    total_amount: float
    status: str
    expires_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderResponseList(BaseModel):
    orders: list[OrderResponse]

    model_config = ConfigDict(from_attributes=True)
