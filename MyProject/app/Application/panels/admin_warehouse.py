from abc import ABC
from Application.interfaces.panel_interface import IAdminWarehousePanel
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


class AdminWarehousePanel(IAdminWarehousePanel, ABC):
    def __init__(self, employee_id):
        self.employee_id = employee_id
        self.warehouse_service = WarehouseService()
        self.registration_service = Registration()
        self.notification_service = NotificationService()
        self.stock_service = StockService()
        self.user_service = UserService()
        self.product_service = ProductService()
        self.product_service = ProductService()
        self.menu_service = Menu("پنل مدیریت انبارها")
        self.menu = Menu(f"پنل ادمین انبار و موجودی")
        self.setup_menu()

    def setup_menu(self) -> None:
        self.menu.add_option("1", "مدیریت انبارها و موجودی ", self._manage_warehouse)

    def show_menu(self) -> None:
        self.menu.display()

    def handle_menu_choice(self, choice: str) -> None:
        if choice in self.menu.options:
            _, action, _ = self.menu.options[choice]
            if action:
                action()

    def _manage_warehouse(self) -> None:
        product_menu = Menu("مدیریت انبار و موجودی")
        product_menu.add_option("1", "ثبت انبار", self._add_warehouse)
        product_menu.add_option("2", "مشاهده همه انبارها", self._list_warehouse)
        product_menu.add_option("3", "جستجوی انبار", self._search_warehouse)
        product_menu.add_option("4", "ویرایش انبار", self._edit_warehouse)
        product_menu.add_option("5", "حذف انبار", self._delete_warehouse)
        product_menu.add_option("6", "ثبت اضافه", self._add_stock)
        product_menu.add_option("7", "ثبت کسری", self._delete_stock)
        product_menu.add_option("8", "گزارش موجودی  کالا ", self._list_warehouses_stocks)
        product_menu.add_option("9", "بازگشت", None, self.menu)
        product_menu.execute()

    # _________________ware house________________________

    def _add_warehouse(self) -> None:
        data = self.registration_service.register_warehouse()
        data = {
            "name": data.get('name'),
            "location": data.get('location'),
            "warehouse_type": data.get('warehouse_type'),
            "branch_name": data.get('branch_name'),
            "created_at": jdatetime.date.today(),
        }
        self.warehouse_service.create_warehouse(data)

    def _list_warehouse(self) -> dict | None:
        data = self.warehouse_service.get_all_warehouse()
        if data is None:
            print("انباری یافت نشد")
            return
        self.display_warehouse(data[0])
        return data[0]

    def _search_warehouse(self) -> None:
        warehouse_id = int(input("لطفا آیدی انبار را وارد کنید "))
        data = self.warehouse_service.get_warehouse_by_id(warehouse_id)
        self.display_warehouse(data)

    def _edit_warehouse(self) -> None:
        warehouse_id = int(input("لطفا آیدی انبار را وارد کنید "))
        warehouse = self.warehouse_service.get_warehouse_by_id(warehouse_id)
        if not warehouse:
            print("محصول یافت نشد.")
            return
        warehouse = warehouse
        print("اطلاعات جدید را وارد کنید (برای حفظ مقدار قبلی خالی بگذارید):")
        name = input(f"نام جدید [{warehouse['name']}]: ") or warehouse['name']
        location = input(f"توضیحات جدید [{warehouse['location']}]: ") or warehouse['location']
        branch_name = input(f"توضیحات جدید [{warehouse['branch_name']}]: ") or warehouse['branch_name']

        updates = {
            'name': name,
            'location': location,
            'branch_name': branch_name
        }

        if self.warehouse_service.update_warehouse(warehouse_id, updates):
            print("محصول با موفقیت بروزرسانی شد.")
        else:
            print("خطا در بروزرسانی محصول.")

    def _delete_warehouse(self) -> None:
        warehouse_id = int(input("لطفا آیدی انبار را وارد کنید "))
        self.warehouse_service.delete_warehouse(warehouse_id)

    def display_warehouse(self, warehouses: Dict) -> None:
        if warehouses:
            print("-" * 50)
            print(f" شناسه انبار:{warehouses['warehouse_id']}")
            print(f" نام انبار:{warehouses['name']}")
            print(f" لوکیشن انبار:{warehouses['location']}")
            print("-" * 50)

    # _________________stocks________________________

    def _add_stock(self):
        warehouse = self._list_warehouse()
        info = self.registration_service.add_stock()
        if not info:
            print("اطلاعات برای اضافه کردن موجودی کالا معتبر نیست")
            return
        product_id = info.get("product_id")
        product = self._search_product(product_id)
        base_price = product[0]["sale_price"]
        sale_price = base_price
        markup_percent = info.get("markup")
        discount_percent = info.get("discount")
        if markup_percent > 0:
            sale_price *= (1 + markup_percent / 100)
        if discount_percent > 0:
            sale_price *= (1 - discount_percent / 100)
        data = {
            "warehouse_id": warehouse.get("warehouse_id"),
            "product_id": product_id,
            "seller_id": info.get("seller_id"),
            "quantity": info.get("quantity"),
            "markup_percent": info.get("markup"),
            "discount_percent": info.get("discount"),
            "sale_price": sale_price,
            "updated_at": jdatetime.date.today().strftime("%Y-%m-%d"),
            "updated_by": self.user_id
        }
        self.stock_service.add_stock(data)

    def _delete_stock(self) -> None:
        stock_id = int(input("لطفا آیدی  موجودی را وارد کنید "))
        stock = self.stock_service.get_stock_by_id(stock_id)
        if not stock:
            print("محصول یافت نشد.")
            return
        stock = stock[0]
        print("اطلاعات جدید را وارد کنید (برای حفظ مقدار قبلی خالی بگذارید):")
        quan = int(input(f"مقدار کسری [{stock['quantity']}]: ") or stock['quantity'])
        quantity = stock['quantity'] - quan
        updates = {
            'quantity': quantity
        }
        if self.stock_service.update_stock(stock_id, updates):
            print("محصول با موفقیت بروزرسانی شد.")
            print(f" : موجودی جدید کالا {quantity}")
        else:
            print("خطا در بروزرسانی محصول.")

    def _warehouses_movement(self):
        print("WAREHOUSES MOVEMENT")

    def _list_warehouses_movement(self):
        print("LIST WAREHOUSES MOVEMENT")

    def _list_warehouses_stocks(self):
        product_id = int(input("لطفا آیدی  کالا را وارد کنید "))
        data = self.stock_service.get_stock_by_product(product_id)
        print(data)
        if data is None:
            print("کالا موجود نمیباشد")
            return
        for warehouse in data:
            print("*" * 50)
            print("____________________موجودی کالا_______________")
            print(f"آیدی کالا: {warehouse.get('product_id')}")
            print(f"موجود در انبار: {warehouse.get('warehouse_id')}")
            print(f"آیدی فروشنده: {warehouse.get('seller_id')}")
            print(f"موجودی: {warehouse.get('quantity')}")
            print("*" * 50)





