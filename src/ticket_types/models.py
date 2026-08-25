from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.core.database import Base, UUIDMixin, TimestampMixin
from src.events.models import Event

if TYPE_CHECKING:
    from src.orders.models import Order


class TicketType(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "ticket_types"

    event_id: Mapped[str] = mapped_column("event_id", ForeignKey("events.id"))
    name: Mapped[str] = mapped_column("name", nullable=False)
    price: Mapped[float] = mapped_column("price", nullable=False)
    quantity_total: Mapped[int] = mapped_column("quantity_total", nullable=False)
    quantity_sold: Mapped[int] = mapped_column("quantity_sold", nullable=True, default=0)
    is_active: Mapped[bool] = mapped_column("is_active", nullable=True, default=True)

    event: Mapped[Event] = relationship(foreign_keys=[event_id], back_populates="ticket_types")
    orders: Mapped[list["Order"]] = relationship(back_populates="ticket_type")
