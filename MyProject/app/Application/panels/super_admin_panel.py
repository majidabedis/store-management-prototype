from abc import ABC
from datetime import datetime
from Application.interfaces.panel_interface import ISuperAdminPanel
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


class SuperAdminPanel(ISuperAdminPanel):
    def __init__(self, employee_id: int):
        self.user_id = employee_id
        self.user_service = UserService()
        self.product_service = ProductService()
        self.order_service = OrderService()
        self.warehouse_service = WarehouseService()
        self.notification_service = NotificationService()
        self.stock_service = StockService()
        self.registration_service = Registration()
        self.system_run = RunSystemService()
        self.get_stock = get_stock
        self.menu = Menu(f"پنل ادمین سسیتم")
        self.setup_menu()

    def setup_menu(self) -> None:
        self.menu.add_option("1", "راه اندازی اولیه سیستم ", self.__run_system)
        self.menu.add_option("2", "مدیریت کاربران", self.manage_users)
        self.menu.add_option("3", "مدیریت محصولات", self.manage_products)
        self.menu.add_option("4", " مدیریت انبار وموجودی ", self.manage_warehouse)
        self.menu.add_option("5", "مدیریت سفارشات", self._manage_orders)
        self.menu.add_option("6", "اعلان‌ها", self.manage_notifications)
        self.menu.add_option("7", "خروج", action=None)

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

    def __run_system(self) -> None:
        self.system_run.create_data_base()

    def manage_users(self) -> None:
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

    def manage_products(self) -> None:
        product_menu = Menu("مدیریت محصولات")
        product_menu.add_option("1", "ثبت محصولات", self.add_product)
        product_menu.add_option("2", "مشاهده همه محصولات", self._list_all_products)
        product_menu.add_option("3", "جستجوی محصول ", self._search_product)
        product_menu.add_option("4", "ویرایش محصول", self._edit_product)
        product_menu.add_option("5", "حذف محصول", self._delete_product)
        product_menu.add_option("6", "بازگشت", None, self.menu)
        product_menu.execute()

    def manage_warehouse(self) -> None:
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

    def manage_notifications(self) -> None:
        notification_menu = Menu("مدیریت اعلان‌ها")
        notification_menu.add_option("1", "مشاهده اعلان‌ها", self._view_notifications)
        notification_menu.add_option("2", "ارسال اعلان جدید", self._send_notification)
        notification_menu.add_option("3", "حذف اعلان", self._delete_notification)
        notification_menu.add_option("4", "بازگشت", None, self.menu)
        notification_menu.execute()

    def _manage_orders(self) -> None:
        order_menu = Menu("مدیریت سفارشات")
        order_menu.add_option("1", "مشاهده همه سفارشات", self._list_all_orders)
        order_menu.add_option("2", "جستجوی سفارش", self._search_order)
        order_menu.add_option("3", "تغییر وضعیت سفارش", self._update_order_status)
        order_menu.add_option("4", "بازگشت", None, self.menu)
        order_menu.execute()

    def _view_notifications(self) -> None:
        self.notification_service.view_notification_mongo()

    def _send_notification(self) -> None:
        title = input("عنوان اعلان را وارد کنید: ")
        message = input("پیام اعلان را وارد کنید: ")
        user_id = input("شناسه کاربر را وارد کنید (برای همه کاربران خالی بگذارید): ")
        print(f"{title}: {message} for {user_id}")
        user_id = int(user_id)
        notif = {
            "user_id": user_id,
            "title": title,
            "message": message,
            "create_at": datetime.now(),
        }
        if self.notification_service.create_notification_mongo(notif):
            print("اعلان با موفقیت ارسال شد.")
        else:
            print("خطا در ارسال اعلان.")

    def _delete_notification(self) -> None:
        notification_id = input("شناسه اعلان را وارد کنید: ")
        if self.notification_service.delete_notification_mongo(notification_id):
            print("اعلان با موفقیت حذف شد.")
        else:
            print("خطا در حذف اعلان.")

    # _________________________user section_________________________

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
        status = input(f"وضعیت جدید [{user['status']}]: ") or user['status']
        position = user["position"]
        user_id = user.get(f"{position}_id", "نامشخص")
        updates = {
            'name': name,
            'email': email,
            'status': status
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

    # ____________product section________________

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
        location = input(f"آدرس جدید [{warehouse['location']}]: ") or warehouse['location']
        branch_name = input(f"شعبه جدید [{warehouse['branch_name']}]: ") or warehouse['branch_name']

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
        if data is None:
            print("کالا موجود نمیباشد")
            return
        for warehouse in data:
            print("*" * 50)
            print(f"____________________{warehouse.get('stock_id')} :موجودی کالا _______________")
            print(f"آیدی موجودی: {warehouse.get('stock_id')}")
            print(f"آیدی کالا: {warehouse.get('product_id')}")
            print(f"موجود در انبار: {warehouse.get('warehouse_id')}")
            print(f"آیدی فروشنده: {warehouse.get('seller_id')}")
            print(f"موجودی: {warehouse.get('quantity')}")
            print("*" * 50)

        # _________________order________________________

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
