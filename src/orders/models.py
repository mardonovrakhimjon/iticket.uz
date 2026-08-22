from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Numeric, String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base, UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from src.users.models import User
    from src.tickets.models import TicketType  


class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class Order(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "orders"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    ticket_type_id: Mapped[str] = mapped_column(ForeignKey("ticket_types.id"), nullable=False)
    
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    
    status: Mapped[OrderStatus] = mapped_column(
        String, 
        nullable=False, 
        default=OrderStatus.PENDING
    )
    
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    user: Mapped["User"] = relationship(
        foreign_keys=[user_id], 
        back_populates="orders"
    )
    
    ticket_type: Mapped["TicketType"] = relationship(
        foreign_keys=[ticket_type_id], 
        back_populates="orders"
    )
