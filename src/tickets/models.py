from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.core.database import Base, UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from src.events.models import Event
    from src.orders.models import Order
    from src.ticket_types.models import TicketType
    from src.users.models import User


class TicketStatus(str, Enum):
    VALID = "valid"
    USED = "used"
    CANCELLED = "cancelled"


class Ticket(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "tickets"

    order_id: Mapped[str] = mapped_column("order_id", ForeignKey("orders.id"))
    ticket_type_id: Mapped[str] = mapped_column("ticket_type_id", ForeignKey("ticket_types.id"))
    event_id: Mapped[str] = mapped_column("event_id", ForeignKey("events.id"))
    owner_user_id: Mapped[str] = mapped_column("owner_user_id", ForeignKey("users.id"))
    status: Mapped[TicketStatus] = mapped_column(
        "status", default=TicketStatus.VALID, nullable=True
    )
    issued_at: Mapped[datetime] = mapped_column("issued_at", default=datetime.now, nullable=True)
    used_at: Mapped[datetime] = mapped_column("used_at", nullable=True, default=None)
    checked_in_by_id: Mapped[str] = mapped_column(
        "checked_in_by_id", ForeignKey("users.id"), nullable=True
    )

    order: Mapped["Order"] = relationship(foreign_keys=[order_id], back_populates="tickets")
    ticket_type: Mapped["TicketType"] = relationship(
        foreign_keys=[ticket_type_id], back_populates="tickets"
    )
    event: Mapped["Event"] = relationship(foreign_keys=[event_id], back_populates="tickets")
    owner_user: Mapped["User"] = relationship(
        foreign_keys=[owner_user_id], back_populates="tickets"
    )
    checked_in_by: Mapped["User"] = relationship(
        foreign_keys=[checked_in_by_id], back_populates="checked_tickets"
    )
