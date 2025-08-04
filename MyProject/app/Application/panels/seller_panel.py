from abc import ABC
from datetime import datetime
from typing import Dict, List, Optional
from Application.interfaces.panel_interface import ISellerPanel
from Application.services.user_service import SellerService
from Application.services.product_service import ProductService
from Application.services.order_service import OrderService
from Application.services.stock_service import StockService
from Application.services.notification_service import NotificationService
from utils.Registration import Registration
from utils.input_utils import get_stock
from Presentation.menu import Menu


class SellerPanel(ISellerPanel, ABC):
    def __init__(self, seller_id: int):
        self.seller_id = seller_id
        self.seller_service = SellerService()
        self.product_service = ProductService()
        self.order_service = OrderService()
        self.notification_service = NotificationService()
        self.registration_service = Registration()
        self.stock_service = StockService()
        self.menu = Menu("پنل فروشنده")
        self.setup_menu()

    def setup_menu(self) -> None:
        self.menu.add_option("1", "مدیریت محصولات", self.manage_products)
        self.menu.add_option("2", "مدیریت سفارشات", self.manage_orders)
        self.menu.add_option("3", "اعلان‌ها", self.view_notifications)
        self.menu.add_option("4", "خروج", exit)

    def show_menu(self) -> None:
        self.menu.display()

    def handle_menu_choice(self, choice: str) -> None:
        if choice in self.menu.options:
            _, action, _ = self.menu.options[choice]
            if action:
                action()

    def manage_products(self) -> None:
        product_menu = Menu("مدیریت محصولات")
        product_menu.add_option("1", "مشاهده لیست محصولات", self._list_products)
        product_menu.add_option("2", "افزودن محصول جدید", self._add_product)
        product_menu.add_option("3", "ویرایش محصول", self._edit_product_temp)
        product_menu.add_option("4", "حذف محصول", self._delete_product)
        product_menu.add_option("5", "بازگشت", None, self.menu)
        product_menu.execute()

    def manage_orders(self) -> None:
        order_menu = Menu("مدیریت سفارشات")
        order_menu.add_option("1", "مشاهده سفارشات", self._list_orders)
        order_menu.add_option("2", "تغییر وضعیت سفارش", self._update_order_status)
        order_menu.add_option("3", "بازگشت", None, self.menu)
        order_menu.execute()

    def view_notifications(self) -> None:
        notifications = self.notification_service.get_user_notifications(self.seller_id)
        if notifications:
            for notification in notifications:
                print(f"عنوان: {notification['title']}")
                print(f"پیام: {notification['message']}")
                print(f"تاریخ: {notification['created_at']}")
                print("-" * 50)
        else:
            print("هیچ اعلانی یافت نشد.")

    def _list_products(self) -> None:
        products = self.product_service.get_seller_products(self.seller_id)
        self._display_products(products)

    def _add_product(self) -> None:
        data = self.registration_service.register_product()
        add = self.product_service.create_product_temp(data, self.seller_id)

        if add:
            notif = {
                "user_id": 1,
                "title": "اضافه کردن محصول",
                "message": f" محصول{add}  فروشنده توسط {self.seller_id} ایجاد شده است ",
                "create_at": datetime.now(),
            }
            self.notification_service.create_notification_mongo(notif)
            print("  اطلاعات ثبت شد ،بعد از تایید ادمین به لیست کالاهای فعال اضافه میشود ")
            return

    def _edit_product_temp(self) -> None:
        product_temp_id = int(input("شناسه محصول را وارد کنید: "))
        product = self._search_product(product_temp_id)
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
        updates = {
            'name': name,
            'brand': brand,
            'model': model,
            'price': price,
            'description': description,
            'color': color,
        }

        if self.product_service.update_product_temp(product_temp_id, updates):
            print("محصول با موفقیت بروزرسانی شد.")
        else:
            print("خطا در بروزرسانی محصول.")

    def _search_product(self, product_temp_id: int = None) -> list[dict] | None:
        condition = None
        if not product_temp_id:
            print(" 1:بر اساس آیدی  ")
            print(" 2: براساس نام کالا ")
            print(" 3: براساس دسته بندی ")
            print(" 4: براساس رنگ کالا ")
            choice = input(": (بر چه اساس می خواهید جستجو کنید؟(شماره را وارد نمایید")
            if choice == "1":
                product_temp_id = int(input("آیدی محصول را وارد کنید: "))
                condition = f"product_temp_id = '{product_temp_id}'"
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
        elif product_temp_id:
            condition = f" product_temp_id = '{product_temp_id}' AND seller_id = '{self.seller_id}'"
        else:
            condition = None

        try:
            products = self.product_service.search_product_temp(condition)
            self._display_products(products)
            return products
        except ValueError:
            print("آیدی وارد شده نامعتبر است.")

    def _display_products(self, products: List[Dict]) -> None:
        if products:
            for product in products:
                print(f"*******مشخصات کالای کد {product.get("product_id")}*********")
                product_id = product.get("product_temp_id")
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

    def _delete_product(self) -> None:
        product_temp_id = int(input("آیدی محصول را وارد کنید: "))
        self.product_service.delete_product_temp(product_temp_id)

    def _list_orders(self) -> None:
        stocks = self.stock_service.get_stock_by_seller_id(self.seller_id)[0]
        stock_id = stocks.get("stock_id")
        orders = self.order_service.get_seller_orders(stock_id)

        if orders:
            for order in orders:
                print(f"شناسه سفارش: {order['order_id']}")
                print(f"شناسه محصول: {order['product_id']}")
                print(f" تعداد: {order['quantity']}")
                print(f"قیمت: {order['price']}")
                print("-" * 50)
        else:
            print("هیچ سفارشی یافت نشد.")

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

    def manage_complaints(self) -> None:
        pass

    def view_reports(self) -> None:
        pass

    def manage_profile(self) -> None:
        pass

    def view_orders(self) -> None:
        pass

    def _view_shop_info(self) -> None:
        shop_info = self.seller_service.get_user_by_id(self.seller_id, "seller")
        if shop_info:
            print("\n=== اطلاعات فروشگاه ===")
            print(f"نام فروشگاه: {shop_info['shop_name']}")
            print(f"نام فروشنده: {shop_info['name']}")
            print(f"ایمیل: {shop_info['email']}")
            print(f"موبایل: {shop_info['mobile']}")
            print(f"آدرس: {shop_info['address']}")
        else:
            print("خطا در دریافت اطلاعات فروشگاه")

    def _edit_shop_info(self) -> None:
        pass

    def _change_password(self) -> None:
        pass
