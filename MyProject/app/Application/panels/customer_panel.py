from typing import Dict, List, Optional
import bcrypt
from Application.interfaces.panel_interface import ICustomerPanel
from Application.services.user_service import UserService
from Application.services.product_service import ProductService
from Application.services.cart_service import CartService
from Application.services.order_service import OrderService
from Application.services.notification_service import NotificationService
from Application.services.paid_service import PaidService
from Application.services.invoice_service import InvoiceService
from Application.services.stock_service import StockService
from Presentation.menu import Menu
import json


class CustomerPanel(ICustomerPanel):
    def __init__(self, customer_id: int):
        self.user_id = customer_id
        self.user_service = UserService()
        self.product_service = ProductService()
        self.cart_service = CartService()
        self.order_service = OrderService()
        self.notification_service = NotificationService()
        self.paid_service = PaidService()
        self.invoice_service = InvoiceService()
        self.stock_service = StockService()
        self.menu = Menu("پنل مشتری")
        self.setup_menu()

    def setup_menu(self) -> None:
        self.menu.add_option("1", "مشاهده محصولات", self.view_products)
        self.menu.add_option("2", "مدیریت سبد خرید", self.manage_cart)
        self.menu.add_option("3", "مدیریت سفارشات", self._manage_orders)
        self.menu.add_option("4", "پروفایل", self.view_profile)
        self.menu.add_option("5", "اعلان‌ها", self._view_notifications)
        self.menu.add_option("6", "خروج", None)

    def show_menu(self) -> None:
        self.menu.display()

    def handle_menu_choice(self, choice: str) -> None:
        if choice in self.menu.options:
            label, action, _ = self.menu.options[choice]
            if action:
                action()

    def view_products(self) -> None:
        product_menu = Menu("مشاهده محصولات")
        product_menu.add_option("1", "مشاهده همه محصولات", self._list_all_products)
        product_menu.add_option("2", "جستجوی محصول", self._search_product)
        product_menu.add_option("3", "مشاهده جزئیات محصول", self._view_product_details)
        product_menu.add_option("4", "بازگشت", None, self.menu)
        product_menu.execute()

    def manage_cart(self) -> None:
        cart_menu = Menu("مدیریت سبد خرید")
        cart_menu.add_option("1", "مشاهده سبد خرید", self._view_cart)
        cart_menu.add_option("2", "افزودن محصول به سبد", self._add_to_cart)
        cart_menu.add_option("3", "حذف محصول از سبد", self._remove_from_cart)
        cart_menu.add_option("4", "تغییر تعداد محصول", self._update_cart_item)
        cart_menu.add_option("5", "تکمیل خرید", self._checkout)
        cart_menu.add_option("6", "بازگشت", None, self.menu)
        cart_menu.execute()

    def view_profile(self) -> None:
        profile_menu = Menu("پروفایل")
        profile_menu.add_option("1", "مشاهده اطلاعات", self._view_profile_info)
        profile_menu.add_option("2", "ویرایش اطلاعات", self.edit_profile)
        profile_menu.add_option("3", "بازگشت", None, self.menu)
        profile_menu.execute()

    def _manage_orders(self) -> None:
        order_menu = Menu("مدیریت سفارشات")
        order_menu.add_option("1", "مشاهده تاریخچه سفارشات", self._list_orders)
        order_menu.add_option("2", "مشاهده جزئیات سفارش", self._view_order_details)
        order_menu.add_option("3", "لغو سفارش", self._cancel_order)
        order_menu.add_option("4", "بازگشت", None, self.menu)
        order_menu.execute()

    def edit_profile(self) -> None:
        user = self.user_service.get_user_by_id(self.user_id, "customer")
        if not user:
            print("کاربر یافت نشد.")
            return

        print("اطلاعات جدید را وارد کنید (برای حفظ مقدار قبلی خالی بگذارید):")
        name = input(f"نام جدید [{user['name']}]: ") or user['name']
        email = input(f"ایمیل جدید [{user['email']}]: ") or user['email']
        mobile = input(f"موبایل جدید [{user['mobile']}]: ") or user['mobile']
        password = input("رمز عبور جدید (برای حفظ رمز قبلی خالی بگذارید): ") or user['password']
        raw_password = password
        if raw_password:
            hashed = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
            password = hashed.decode('utf-8')

        updates = {
            'name': name,
            'email': email,
            'password': password,
            'mobile': mobile

        }
        if password:
            updates['password'] = password

        if self.user_service.update_user("customer", self.user_id, updates):
            print("پروفایل با موفقیت بروزرسانی شد.")
        else:
            print("خطا در بروزرسانی پروفایل.")

    def _view_notifications(self) -> None:
        notifications = self.notification_service.get_user_notifications(self.user_id)
        if notifications:
            for notification in notifications:
                print(f"عنوان: {notification['title']}")
                print(f"پیام: {notification['message']}")
                print(f"تاریخ: {notification['created_at']}")
                print("-" * 50)
        else:
            print("هیچ اعلانی یافت نشد.")

    def _list_all_products(self) -> None:
        products = self.product_service.get_all_products()
        self._display_products(products)

    def _search_product(self, product_id: int = None) -> list[dict] | None:
        if not product_id:
            search_term = input("آیدی محصول را وارد کنید: ")
        else:
            search_term = product_id
        try:
            products = self.product_service.get_product_by_id(int(search_term))
            self._display_products(products)
            return products
        except ValueError:
            print("آیدی وارد شده نامعتبر است.")

    def _view_product_details(self) -> None:
        product_id = int(input("شناسه محصول را وارد کنید: "))
        product = self.product_service.get_product_by_id(product_id)
        if product:
            product = product[0]
            product_spect = json.loads(product.get('product_spect'))
            specs = product_spect[0]
            category = product['category']
            if category == "mobile":
                print(f"شناسه: {product['product_id']}")
                print(f"نام: {product['name']}")
                print(f"برند: {product['brand']}")
                print(f"مدل: {product['model']}")
                print(f"رنگ: {product['color']}")
                print(f"پردازنده: {specs['processor']}")
                print(f"سیستم عامل: {specs['os']}")
                print(f"قیمت: {product['sale_price']}")
                print(f"توضیحات: {product['description']}")
            elif category == "camera":
                print(f"شناسه: {product_id}")
                print(f"نام: {product['name']}")
                print(f"برند: {product['brand']}")
                print(f"مدل: {product['model']}")
                print(f"رنگ: {product['color']}")
                print(f"سنسور: {specs['sensor_type']}")
                print(f"سایز سنسور: {specs['sensor_size']}")
                print(f"رزولوشن: {specs['resolution']}")
                print(f"مدل لنز: {specs['lens_type']}")
                print(f"محدوده ایزو: {specs['iso_range']}")
                print(f"سرعت شات: {specs['shutter_speed']}")
                print(f"کیفیت ویدیو: {specs['video_resolution']}")
                print(f"قیمت: {product['sale_price']}")
                print(f"توضیحات: {product['description']}")
            elif category == "laptop":
                print(f"شناسه: {product_id}")
                print(f"نام: {product['name']}")
                print(f"برند: {product['brand']}")
                print(f"مدل: {product['model']}")
                print(f"رنگ: {product['color']}")
                print(f"اندازه صفحه: {specs['screen_size']}")
                print(f"پردازنده: {specs['processor']}")
                print(f" رم: {specs['ram']}")
                print(f"هارد: {specs['storage']}")
                print(f"کارت گرافیک: {specs['graphics_card']}")
                print(f"عمر باطری: {specs['battery_life']}")
                print(f"وزن: {specs['weight']}")
                print(f"سیستم عامل: {specs['os']}")
                print(f"توضیحات: {product['description']}")
            add_to_cart = input("آیا می‌خواهید این محصول را به سبد خرید اضافه کنید؟ (بله/خیر): ")
            if add_to_cart.lower() == 'بله':
                quantity = int(input("تعداد مورد نظر را وارد کنید: "))
                self._add_to_cart(product_id, quantity)
        else:
            print("محصول یافت نشد.")

    def _display_products(self, products: List[Dict]) -> None:
        if products:
            for product in products:
                print(f"_________مشخصات کالای کد : {product['product_id']}__________")
                print(f"شناسه: {product['product_id']}")
                print(f"نام: {product['name']}")
                print(f"دسته بندی: {product['category']}")
                print(f"برند: {product['brand']}")
                print(f"مدل: {product['model']}")
                print(f"رنگ: {product['color']}")
                print(f"توضیحات: {product['description']}")
                print(f"قیمت: {product['sale_price']}")
                print("*" * 50)
        else:
            print("هیچ محصولی یافت نشد.")

    def _view_cart(self) -> None:
        self.cart_service.get_cart(self.user_id)

    def _add_to_cart(self, product_id: Optional[int] = None, quantity: Optional[int] = None) -> None:
        if product_id is None:
            product_id = int(input("شناسه محصول را وارد کنید: "))
            quantity = int(input("تعداد محصول را وارد کنید: "))
        product = self.stock_service.get_stock_by_product(product_id)[0]
        stock = product.get('quantity')

        if not product and stock >= quantity:
            print("محصول یافت نشدی یا موجودی کافی نمی باشد.")
            return
        cart = self.cart_service.add_to_cart(self.user_id, product_id, quantity)
        if cart:
            print("سبد خرید ایجاد شد")
        else:
            print("ساخت سبد خرید ناموفق بود ")

    def _remove_from_cart(self) -> None:
        if self.cart_service.remove_from_cart(self.user_id):
            print("محصول با موفقیت از سبد خرید حذف شد.")
        else:
            print("خطا در حذف محصول از سبد خرید.")

    def _update_cart_item(self) -> None:
        quantity = int(input("تعداد برای کم یا زیاد شدن وارد نمایید"))
        inc = input("1.اضافه شود \n 2.کم شود \n")
        if self.cart_service.update_cart_item(self.user_id, quantity, inc):
            print("تعداد محصول با موفقیت بروزرسانی شد.")
        else:
            print("خطا در بروزرسانی تعداد محصول.")

    def _checkout(self) -> None:
        add_order = self.order_service.create_order(self.user_id)
        orders = self.order_service.get_all_orders()
        pending = [o for o in orders if o['status'] == 'pending' and o['customer_id'] == self.user_id]
        if not pending:
            print("هیچ سفارشی در حالت انتظار وجود ندارد.")
            return

        print("سفارش‌های در حال انتظار:")
        for idx, order in enumerate(pending, start=1):
            print(f"{idx}. سفارش شماره {order['order_id']} - مبلغ: {order['total_amount']}")

        if input("آیا مایل به پرداخت هستید؟ (بله/خیر) ").strip() != "بله":
            print("لطفا در اسرع وقت پرداخت انجام دهید.")
            return

        try:
            choice = int(input("شماره سفارش مورد نظر را وارد کنید: ")) - 1
            selected = pending[choice]
        except (ValueError, IndexError):
            print("ورودی نامعتبر است.")
            return

        order_id = selected['order_id']
        o_item = self.order_service.get_order_items_by_order_id(order_id)
        print(o_item)
        print(selected)
        product_id = o_item.get('product_id')
        print(f"شما سفارش شماره {order_id} با مبلغ {selected['total_amount']} را انتخاب کردید.")

        paid = self.paid_service.process_payment(self.user_id, order_id)
        if not paid:
            print("پرداخت انجام نشد.")
            return

        self.order_service.update_order_status(order_id, "paid")
        paid_id = paid[1]
        paid_info = self.paid_service.get_paid_by_id(paid_id)[0]
        self.invoice_service.create_invoice(
            self.user_id,
            order_id,
            paid_id,
            selected['total_items'],
            selected['total_amount'],
        )
        self.invoice_service.show_factor(product_id, order_id)

    def _list_orders(self) -> None:
        orders = self.order_service.get_user_orders(self.user_id)
        if orders:
            for order in orders:
                print(f"شناسه سفارش: {order['order_id']}")
                print(f"وضعیت: {order['status']}")
                print(f"تاریخ: {order['order_date']}")
                print("-" * 50)
        else:
            print("هیچ سفارشی یافت نشد.")

    def _view_order_details(self) -> None:
        order_id = int(input("شناسه سفارش را وارد کنید: "))
        order = self.order_service.get_order_by_id(order_id)
        if order and order['customer_id'] == self.user_id:
            print(f"شناسه سفارش: {order['order_id']}")
            print(f"وضعیت: {order['status']}")
            print(f"تاریخ: {order['order_date']}")
            total = 0
            print(f"مجموع: {order['total_amount']}")
            print("-" * 50)
        else:
            print("سفارش یافت نشد.")

    def _cancel_order(self) -> None:
        order_id = int(input("شناسه سفارش را وارد کنید: "))
        if self.order_service.cancel_order(order_id, self.user_id):
            print("سفارش با موفقیت لغو شد.")
        else:
            print("خطا در لغو سفارش.")

    def _view_profile_info(self) -> None:
        user = self.user_service.get_user_by_id(self.user_id, "customer")
        if user:
            print("*********** مشخصات *************")
            print(f"نام: {user['name']}")
            print(f"نام: {user['family']}")
            print(f"ایمیل: {user['email']}")
            print(f"موبایل: {user['mobile']}")
            print(f"تاریخ تولد: {user['birthday']}")
            print(f"آدرس: {user['address']}")
            print(f"موجودی کف پول:{user['digital_wallet']}")
            print("-" * 50)
        else:
            print("کاربر یافت نشد.")
