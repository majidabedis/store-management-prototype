from Database.repositories.order_repository import OrderRepository
from Database.repositories.order_item_repository import OrderItemRepository

user_id = 60000001
order_repository = OrderRepository()
order_item_repository = OrderItemRepository()


def process_payment(user_id: int) -> None:
    pass
    # orders = order_repository.get_all()
    # pending_orders = [order for order in orders if order.get('status') == 'pending']
    #
    # if not pending_orders:
    #     print("هیچ سفارشی در حالت انتظار وجود ندارد.")
    #     return
    #
    # print("سفارش‌های در حال انتظار:")
    # for idx, order in enumerate(pending_orders, start=1):
    #     print(f"{idx}. سفارش شماره {order.get('order_id')} - مبلغ: {order.get('total_amount')}")
    #
    # try:
    #     choice = int(input("شماره سفارشی که می‌خواهید پرداخت کنید وارد کنید: "))
    #     selected_order = pending_orders[choice - 1]
    # except (ValueError, IndexError):
    #     print("ورودی نامعتبر است.")
    #     return
    #
    # print(f"شما سفارش شماره {selected_order.get('order_id')} با مبلغ {selected_order.get('total_amount')} را انتخاب کردید.")
    # bank = input("لطفاً شماره کارت را وارد کنید: ")
    # if bank == "11111":
    #     print("بانک ملت انتخاب شد.")
    # else:
    #     print("بانک نامشخص است.")
    #
    # confirm = input("آیا مطمئن هستید که می‌خواهید پرداخت را انجام دهید؟ (yes/no): ")
    # if confirm.lower() == "yes":
    #     selected_order['status'] = 'PAID'
    #     print("پرداخت با موفقیت انجام شد.")
    # elif confirm.lower() == "no":
    #     print("پرداخت لغو شد.")
    # else:
    #     print("ورودی نامعتبر.")

process_payment(user_id)