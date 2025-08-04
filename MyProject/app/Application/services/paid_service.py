from typing import Dict, List, Optional
import jdatetime
from Database.repositories.paid_repository import PaidRepository


class PaidService:
    def __init__(self):
        self.paid_repository = PaidRepository()

    def process_payment(self, user_id: int, pending_orders: int) -> Optional[bool]:
        paid = False
        bank = input("لطفاً شماره کارت را وارد کنید: ")
        if bank.startswith("603799"):
            print("کارت شما متعلق به بانک ملی است")
        elif bank.startswith("589210"):
            print("کارت شما متعلق به بانک سپه است")
        elif bank.startswith("627212"):
            print("کارت شما متعلق به بانک اقتصاد نوین است")
        else:
            print("بانک نامشخص است.")
        confirm = input("آیا مطمئن هستید که می‌خواهید پرداخت را انجام دهید؟ (بله/خیر): ")
        if confirm.lower() == "بله":
            paid = self.create_paid(user_id, pending_orders)
        elif confirm.lower() == "خیر":
            print("پرداخت لغو شد.")
        else:
            print("ورودی نامعتبر.")
        return paid if paid else False

    def create_paid(self, customer_id: int, order_id: int) -> bool | None:
        if customer_id is None and order_id is None:
            print("پرداخت با خطا مواجه شد!!!")
            return
        data = {
            "customer_id": customer_id,
            "order_id": order_id,
            "status": "paid",
        }
        paid = self.paid_repository.add(data)

        return paid if paid else None

    def get_all_paid(self) -> list[dict]:
        return self.paid_repository.get_all()

    def get_paid_by_id(self, payment_id) -> Optional[dict]:
        return self.paid_repository.get_by_id(payment_id)
