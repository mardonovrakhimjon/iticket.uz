from random import randint


class DemoProvider:
    def __init__(self, order_id: str) -> None:
        self.order_id = order_id

    def pay(self, amount: float, card_number: str, ex: str):
        return True

    def verify(self, otp: int):
        if otp == 1234:
            return True
        else:
            return False
