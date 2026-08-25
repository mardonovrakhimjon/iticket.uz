from uuid import UUID

from fastapi import APIRouter, Depends

from src.core.database import AsyncSession, get_db
from src.orders.models import Order
from src.auth.dependencies import get_current_active_user
from src.users.models import User

from src.orders.schemas import OrderCreate, OrderResponse, OrderResponseList
from src.orders.service import OrderService
from src.orders.repository import OrderRepository


router = APIRouter()


@router.post("/", response_model=OrderResponse)
async def create_order(
    data: OrderCreate,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Order:
    service = OrderService(OrderRepository(db))
    return await service.create_order(data, user)  # type: ignore


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: UUID,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Order | None:
    service = OrderService(OrderRepository(db))
    order = await service.get_order(order_id)  # type: ignore
    return order


@router.get("/", response_model=OrderResponseList)
async def get_order_list(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> list[Order]:
    service = OrderService(OrderRepository(db))
    orders = await service.get_orders(user)  # type: ignore
    return OrderResponseList(orders=orders)  # type: ignore


# @router.post('/{order_id}/cancel', response_model=OrderResponse)
# async def cancel_order(
#     order_id: UUID,
#     user: User = Depends(get_current_active_user),
#     db: AsyncSession = Depends(get_db),
# ) -> Order:
#     pass
