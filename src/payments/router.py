from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict

from src.core.database import AsyncSession, get_db
from src.orders.models import Order, OrderStatus
from src.auth.dependencies import get_current_active_user
from src.users.models import User
from src.orders.service import OrderService
from src.orders.schemas import OrderResponse
from src.orders.repository import OrderRepository
from src.payments.service import PaymentService


router = APIRouter()


class Card(BaseModel):
    number: str
    expiry: str


class PayRequest(BaseModel):
    order_id: UUID
    card: Card


class OTPRequest(BaseModel):
    otp: int
    order_id: UUID


class PayResponse(BaseModel):
    status: str
    order: OrderResponse

    model_config = ConfigDict(from_attributes=True)


@router.post("/demo/pay", response_model=PayResponse)
async def pay_demo(
    data: PayRequest,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> PayResponse:
    order_service = OrderService(OrderRepository(db))
    order = await order_service.get_order(data.order_id)

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")

    if order.status == OrderStatus.PAID:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="already paid")

    if order.status == OrderStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="order has been cancelled"
        )

    if order.expires_at < datetime.now():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order expired")

    payment_service = PaymentService(order)
    result = payment_service.pay_demo(data.card)
    if result:
        return PayResponse(status="success", order=order)  # type: ignore

    return PayResponse(status="error", order=order)  # type: ignore


@router.post("/demo/verify", response_model=PayResponse)
async def verify_demo(
    data: OTPRequest,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> PayResponse:
    order_service = OrderService(OrderRepository(db))
    order = await order_service.get_order(data.order_id)

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")

    if order.status == OrderStatus.PAID:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="already paid")

    if order.status == OrderStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="order has been cancelled"
        )

    if order.expires_at < datetime.now():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order expired")

    payment_service = PaymentService(order)
    result = payment_service.verify_demo(data.otp)
    if result:
        order.status = OrderStatus.PAID
        db.add(order)
        await db.commit()

        return PayResponse(status="success", order=order)  # type: ignore

    return PayResponse(status="error", order=order)  # type: ignore
