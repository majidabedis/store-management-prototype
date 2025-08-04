from datetime import datetime

from Application.services.user_service import UserService
from utils.Registration import Registration
from Application.services.notification_service import NotificationService
from Application.panels.panel_dispatcher import PanelDispatcher
from Presentation.menu import Menu


class MainMenu:
    def __init__(self):
        self.send_notification = NotificationService()
        self.user_service = UserService()
        self.registration_inputs = Registration()
        self.main_menu = Menu("فروشگاه آنلاین")
        self.setup_menus()

    def setup_menus(self):
        # ********** main menu **********
        self.main_menu.add_option("1", "ورود به سیستم", self._handle_login)
        self.main_menu.add_option("2", "ثبت نام مشتری", self._customer_registration)
        self.main_menu.add_option("3", "ثبت نام فروشنده", self._seller_registration)
        self.main_menu.add_option("4", "خروج", self._exit_program)

    def _handle_login(self) -> None:
        username = input("نام کاربری: ")
        password = input("رمز عبور: ")
        user = self.user_service.login_user(username, password)
        if not user:
            return
        position = user["position"]
        user_id_key = "employee_id" if position == "super_admin" else f"{position}_id"
        user_id = user.get(user_id_key)
        panel = PanelDispatcher.dispatch(position, user_id)
        if not panel:
            print("خطا در ایجاد پنل کاربری")
            return
        else:
            panel.show_menu()
            while True:
                choice = input("لطفاً گزینه مورد نظر را انتخاب کنید: ")

                panel.handle_menu_choice(choice)

    def _customer_registration(self):
        data = self.registration_inputs.register_customer()
        user = self.user_service.create_user("customer", data)
        if user:
            print("ثبت نام با موفقیت انجام شد")
        else:
            print("خطا در ثبت نام")

    def _seller_registration(self):
        data = self.registration_inputs.register_seller()
        user = self.user_service.create_user("seller", data)
        if user:
            notif = {
                "user_id": 50000001,
                "title": f"seller {data[1]} {data[2]} registered ",
                "message": f"{data[1]} {data[2]} __ email: {data[3]} has been Registered. We are waiting for your acceptance.",
                "create_at": datetime.now()
            }
            self.send_notification.create_notification_mongo(notif)
            print("ثبت نام با موفقیت انجام شد.\n بعد از تایید توسط ادمین اکانت کاربری شما فعال خواهد شد ")

        else:
            print("خطا در ثبت نام")

    def _exit_program(self):
        print("خداحافظ!")
        exit(0)

    def run(self):
        while True:
            self.main_menu.execute()
