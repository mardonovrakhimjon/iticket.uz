from src.orders.models import Order

from src.payments.providers.demo import DemoProvider


class PaymentService:
    def __init__(self, order: Order) -> None:
        self.order = order

    def pay_demo(self, card) -> bool:
        demo_provider = DemoProvider(str(self.order.id))
        amount = self.order.total_amount
        return demo_provider.pay(amount, card.number, card.expiry)

    def verify_demo(self, otp) -> bool:
        demo_provider = DemoProvider(str(self.order.id))
        return demo_provider.verify(otp)

    def pay_payme(self) -> bool:
        pass

    def pay_click(self) -> bool:
        pass
