from abc import ABC
from Application.interfaces.panel_interface import IAdminOrdersPanel
from Application.services.sys_boot import RunSystemService
from Application.services.stock_service import StockService
from Application.services.user_service import UserService
from Application.services.product_service import ProductService
from Application.services.warehouse_service import WarehouseService
from Application.services.order_service import OrderService
from Application.services.notification_service import NotificationService
from Presentation.menu import Menu
from utils.Registration import Registration
from utils.input_utils import get_stock
from typing import List, Dict
from tabulate import tabulate
import jdatetime


class AdminOrderPanel(IAdminOrdersPanel):
    def __init__(self, employee_id):
        self.employee_id = employee_id
        self.order_service = OrderService()
        self.stock_service = StockService()
        self.user_service = UserService()
        self.product_service = ProductService()
        self.menu = Menu(f"پنل ادمین سسیتم")
        self.setup_menu()

    def setup_menu(self) -> None:
        self.menu.add_option("1", "مدیریت سفارشها", self._manage_orders)

    def show_menu(self) -> None:
        self.menu.display()

    def handle_menu_choice(self, choice: str) -> None:
        print(choice)
        if choice in self.menu.options:
            label, action, _ = self.menu.options[choice]
            if action:
                action()
            else:
                print("action not working")

    def _manage_orders(self) -> None:
        order_menu = Menu("مدیریت سفارشات")
        order_menu.add_option("1", "مشاهده همه سفارشات", self._list_all_orders)
        order_menu.add_option("2", "جستجوی سفارش", self._search_order)
        order_menu.add_option("3", "تغییر وضعیت سفارش", self._update_order_status)
        order_menu.add_option("4", "بازگشت", None, self.menu)
        order_menu.execute()

    def _list_all_orders(self) -> None:
        orders = self.order_service.get_all_orders()
        self._display_orders(orders)

    def _search_order(self) -> None:
        order_id = int(input("شناسه سفارش را وارد کنید: "))
        order = self.order_service.get_order_by_id(order_id)
        if order:
            self._display_orders([order])
        else:
            print("سفارش یافت نشد.")

    def _update_order_status(self) -> None:
        order_id = int(input("شناسه سفارش را وارد کنید: "))
        order = self.order_service.get_order_by_id(order_id)

        if not order:
            print("سفارش یافت نشد.")
            return

        print("وضعیت‌های ممکن:")
        print("1. در انتظار پرداخت")
        print("2. پرداخت شده")
        print("3. در حال ارسال")
        print("4. تحویل شده")
        print("5. لغو شده")

        status = int(input("وضعیت جدید را انتخاب کنید: "))
        status_map = {
            1: "pending",
            2: "paid",
            3: "shipping",
            4: "delivered",
            5: "cancelled"
        }

        if status in status_map:
            if self.order_service.update_order_status(order_id, status_map[status]):
                print("وضعیت سفارش با موفقیت بروزرسانی شد.")
            else:
                print("خطا در بروزرسانی وضعیت.")
        else:
            print("وضعیت نامعتبر.")

    def _display_orders(self, orders: List[Dict]) -> None:
        if orders:
            for order in orders:
                print(f"شناسه سفارش: {order['order_id']}")
                print(f"وضعیت: {order['status']}")
                print(f"تاریخ: {order['order_date']}")
                print("-" * 50)
        else:
            print("هیچ سفارشی یافت نشد.")
