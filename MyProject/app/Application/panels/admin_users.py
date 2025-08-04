from abc import ABC
from Application.interfaces.panel_interface import IAdminUsersPanel
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


class AdminUsersPanel(IAdminUsersPanel):
    def __init__(self, employee_id):
        self.employee_id = employee_id
        self.menu_service = Menu("پنل مدیریت پرسنل")
        self.menu = Menu(f"پنل ادمین پرسنل")
        self.setup_menu()
        self.registration_service = Registration()
        self.user_service = UserService()

    def setup_menu(self) -> None:
        self.menu.add_option("1", "مدیریت افراد", self._manage_users)

    def show_menu(self) -> None:
        self.menu.display()

    def handle_menu_choice(self, choice: str) -> None:
        if choice in self.menu.options:
            _, action, _ = self.menu.options[choice]
            if action:
                action()

    def _manage_users(self) -> None:
        user_menu = Menu("مدیریت کاربران")
        user_menu.add_option("1", "ثبت نام مشتری", self.add_customer)
        user_menu.add_option("2", "ثبت نام فروشنده", self.add_seller)
        user_menu.add_option("3", "ثبت نام کارمند", self.add_employee)
        user_menu.add_option("4", "مشاهده همه کاربران", self._list_all_users)
        user_menu.add_option("5", "جستجوی کاربر", self._search_user)
        user_menu.add_option("6", "ویرایش کاربر", self._edit_user)
        user_menu.add_option("7", "حذف کاربر", self._delete_user)
        user_menu.add_option("8", "بازگشت", None, self.menu)
        user_menu.execute()

    def add_customer(self) -> None:
        data = self.registration_service.register_customer()
        if data:
            self.user_service.create_user("customer", data)
        else:
            print("ثبت نام انجام نشد ")

    def add_seller(self) -> None:
        data = self.registration_service.register_seller()
        if data:
            self.user_service.create_user("seller", data)
        else:
            print("ثبت نام انجام نشد ")

    def add_employee(self) -> None:
        data = self.registration_service.register_employee()
        if data:
            print(data)
            self.user_service.create_user("employee", data)
        else:
            print("ثبت نام انجام نشد ")

    def _list_all_users(self) -> None:
        users = self.user_service.get_all_users()
        self._display_users(users)

    def _search_user(self) -> None:
        search_term = input("نام کاربری یا ایمیل را وارد کنید: ")
        users = self.user_service.search_users(search_term)
        self._display_users(users)

    def _edit_user(self) -> None:
        email = input("ایمیل کاربر را وارد کنید: ")
        user = self.user_service.search_users(email)
        if not user:
            print("کاربر یافت نشد.")
            return
        user = user[0]
        print("اطلاعات جدید را وارد کنید (برای حفظ مقدار قبلی خالی بگذارید):")
        name = input(f"نام جدید [{user['name']}]: ") or user['name']
        email = input(f"ایمیل جدید [{user['email']}]: ") or user['email']
        position = input(f"نقش جدید [{user['position']}]: ") or user['position']
        position = user["position"]
        user_id = user.get(f"{position}_id", "نامشخص")
        updates = {
            'name': name,
            'email': email,
            'position': position
        }
        if self.user_service.update_user(position, int(user_id), updates):
            print("کاربر با موفقیت بروزرسانی شد.")
        else:
            print("خطا در بروزرسانی کاربر.")

    def _delete_user(self) -> None:
        user_id = int(input("شناسه کاربر را وارد کنید: "))
        user = self.user_service.get_user_by_id(user_id, " ")
        if not user:
            print("کاربر یافت نشد.")
            return
        confirm = input("آیا از حذف این کاربر اطمینان دارید؟ (بله/خیر): ")
        if confirm.lower() == 'بله':
            if self.user_service.delete_user(" ", user_id):
                print("کاربر با موفقیت حذف شد.")
            else:
                print("خطا در حذف کاربر.")
        else:
            print("عملیات حذف لغو شد.")

    def _display_users(self, users: List[Dict]) -> None:
        if users:
            headers = ["شناسه", "نام", "ایمیل", "نقش"]
            rows = []
            for u in users:
                position = u["position"]
                user_id = u.get(f"{position}_id", "نامشخص")
                rows.append([position, u["email"], u["name"], user_id])

            print(tabulate(rows, headers=headers, tablefmt="grid"))
        else:
            print("هیچ کاربری یافت نشد.")
