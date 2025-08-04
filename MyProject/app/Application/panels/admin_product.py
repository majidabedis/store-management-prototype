from abc import ABC
from Application.interfaces.panel_interface import IAdminProductsPanel
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

class AdminProductPanel(IAdminProductsPanel):
    def __init__(self,employee_id):
        self.employee_id = employee_id
        self.product_service = ProductService()
        self.warehouse_service = WarehouseService()
        self.user_service = UserService()
        self.registration_service = Registration()
        self.menu = Menu(f"پنل ادمین سسیتم")
        self.setup_menu()

    def setup_menu(self) -> None:
        self.menu.add_option("1", "مدیریت محصولات", self.manage_products)


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


    def manage_products(self) -> None:
        product_menu = Menu("مدیریت محصولات")
        product_menu.add_option("1", "ثبت محصولات", self.add_product)
        product_menu.add_option("2", "مشاهده همه محصولات", self._list_all_products)
        product_menu.add_option("3", "جستجوی محصول ", self._search_product)
        product_menu.add_option("4", "ویرایش محصول", self._edit_product)
        product_menu.add_option("5", "حذف محصول", self._delete_product)
        product_menu.add_option("6", "بازگشت", None, self.menu)
        product_menu.execute()

    def add_product(self) -> None:
        data = self.registration_service.register_product()
        self.product_service.create_product(data)

    def _list_all_products(self) -> None:
        products = self.product_service.get_all_products()
        self._display_products(products)

    def _search_product(self, product_id: int = None) -> list[dict] | None:
        condition = None
        if not product_id:
            print(" 1:بر اساس آیدی  ")
            print(" 2: براساس نام کالا ")
            print(" 3: براساس دسته بندی ")
            print(" 4: براساس رنگ کالا ")
            choice = input(": (بر چه اساس می خواهید جستجو کنید؟(شماره را وارد نمایید")
            if choice == "1":
                product_id = int(input("آیدی محصول را وارد کنید: "))
                condition = f"product_id = '{product_id}'"
            elif choice == "2":
                name = input("نام کالا را وارد نمایید").strip()
                condition = f"name = '{name}'"
            elif choice == "3":
                category = input("لطفا دسته بندی کالا را وارد نمایید").strip()
                condition = f"category = '{category}'"
            elif choice == "4":
                color = input("لطفا رنگ مورد نظر راوارد نمایید").strip()
                condition = f"color = '{color}'"
            else:
                print("ورودی نامعتبر است")
                return
        elif product_id:
            condition = f" product_id = '{product_id}'"
        else:
            condition = None

        try:
            products = self.product_service.search_product(condition)
            self._display_products(products)
            return products
        except ValueError:
            print("آیدی وارد شده نامعتبر است.")

    def _edit_product(self) -> None:
        product_id = int(input("شناسه محصول را وارد کنید: "))
        product = self._search_product(product_id)
        if not product:
            print("محصول یافت نشد.")
            return
        product = product[0]
        print("اطلاعات جدید را وارد کنید (برای حفظ مقدار قبلی خالی بگذارید):")
        name = input(f"نام جدید [{product['name']}]: ") or product['name']
        brand = input(f"برند کالا  [{product['brand']}]: ") or product['brand']
        model = input(f"مدل کالا  [{product['model']}]: ") or product['model']
        price = float(input(f"قیمت فروش جدید [{product['sale_price']}]: ") or product['sale_price'])
        description = input(f"توضیحات جدید [{product['description']}]: ") or product['description']
        color = input(f"رنگ کالا  [{product['color']}]: ") or product['color']
        status = input(f"وضعیت کالا  [{product['status']}]: ") or product['status']
        updates = {
            'name': name,
            'brand': brand,
            'model': model,
            'price': price,
            'description': description,
            'color': color,
            'status': status
        }

        if self.product_service.update_product(product_id, updates):
            print("محصول با موفقیت بروزرسانی شد.")
        else:
            print("خطا در بروزرسانی محصول.")

    def _delete_product(self) -> None:
        product_id = int(input("شناسه محصول را وارد کنید: "))
        product = self.product_service.get_product_by_id(product_id)

        if not product:
            print("محصول یافت نشد.")
            return

        confirm = input("آیا از حذف این محصول اطمینان دارید؟ (بله/خیر): ")
        if confirm.lower() == 'بله':
            if self.product_service.delete_product(product_id):
                print("محصول با موفقیت حذف شد.")
            else:
                print("خطا در حذف محصول.")
        else:
            print("عملیات حذف لغو شد.")

    def _display_products(self, products: List[Dict]) -> None:
        if products:
            for product in products:
                print(f"*******مشخصات کالای کد {product.get("product_id")}*********")
                product_id = product.get("product_id")
                print(f"شناسه: {product_id}")
                print(f"نام: {product['name']}")
                print(f"برند: {product['brand']}")
                print(f"مدل: {product['model']}")
                print(f"رنگ: {product['color']}")
                print(f"توضیحات: {product['description']}")
                print(f"دسته‌بندی: {product['parent_category']} ---> {product['category']}")
                print(f"قیمت: {product['sale_price']}")
                print(f"وضعیت: {product['status']}")
                print("-" * 50)
        else:
            print("هیچ محصولی یافت نشد.")