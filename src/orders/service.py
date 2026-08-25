from datetime import datetime, timedelta, timezone
from uuid import UUID
from fastapi import HTTPException, status

from src.orders.repository import OrderRepository
from src.orders.schemas import OrderCreate
from src.users.models import User
from src.orders.models import Order
from src.ticket_types.repository import TicketTypeRepository
from src.core.database import AsyncSessionLocal


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    async def create_order(self, data: OrderCreate, user: User) -> Order | None:

        ticket_type = await TicketTypeRepository(AsyncSessionLocal()).get_ticket_type_by_id(
            data.ticket_type_id
        )
        if not ticket_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="ticket type topilmadi"
            )

        order = Order(
            user_id=user.id,
            ticket_type_id=data.ticket_type_id,
            quantity=data.quantity,
            unit_price=ticket_type.price,
            total_amount=ticket_type.price * data.quantity,
            expires_at=datetime.now() + timedelta(minutes=15),
        )
        return await self.repository.create_order(order)

    async def get_orders(self, user: User) -> list[Order]:
        return await self.repository.get_orders(user.id)

    async def get_order(self, order_id: UUID) -> Order | None:
        return await self.repository.get_order(order_id)

    async def cancel_order(self, order_id: UUID) -> Order | None:
        return await self.repository.cancel_order(order_id)
