from typing import TYPE_CHECKING
from enum import Enum
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.core.database import Base, UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from src.users.models import User
    from src.ticket_types.models import TicketType


class OrderStatus(str, Enum):
    PANDING = "panding"
    PAID = "paid"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class Order(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "orders"

    user_id: Mapped[str] = mapped_column("user_id", ForeignKey("users.id"))
    ticket_type_id: Mapped[str] = mapped_column("ticket_type_id", ForeignKey("ticket_types.id"))
    quantity: Mapped[int] = mapped_column("quantity", nullable=False)
    unit_price: Mapped[float] = mapped_column("unit_price", nullable=False)
    total_amount: Mapped[float] = mapped_column("total_amount", nullable=False)
    status: Mapped[OrderStatus] = mapped_column(
        "status", nullable=True, default=OrderStatus.PANDING
    )
    expires_at: Mapped[datetime] = mapped_column("expires_at", nullable=False)

    user: Mapped["User"] = relationship(foreign_keys=[user_id], back_populates="orders")
    ticket_type: Mapped["TicketType"] = relationship(
        foreign_keys=[ticket_type_id], back_populates="orders"
    )
