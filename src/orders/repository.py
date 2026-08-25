from uuid import UUID

from sqlalchemy import select

from src.core.database import AsyncSession
from src.orders.models import Order


class OrderRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_order(self, order: Order) -> Order:
        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)
        return order

    async def get_orders(self, user_id: UUID) -> list[Order]:
        stmpt = select(Order).where(Order.user_id == user_id)
        orders = await self.db.execute(stmpt)
        return orders.scalars()  # type: ignore

    async def get_order(self, order_id: UUID) -> Order | None:
        stmpt = select(Order).where(Order.id == order_id)
        orders = await self.db.execute(stmpt)
        return orders.scalar_one_or_none()
