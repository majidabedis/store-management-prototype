from typing import Dict, List, Optional
from datetime import datetime, timedelta
import jdatetime
import jdatetime

from Application.interfaces.panel_interface import IEmployeePanel
from Application.services.user_service import EmployeeService
from Application.services.order_service import OrderService
from Application.services.complaint_service import ComplaintService
from Application.services.report_service import ReportService
from Application.services.notification_service import NotificationService
from Application.services.product_service import ProductService

from Presentation.menu import Menu


class EmployeePanel(IEmployeePanel):
    def __init__(self, employee_id: int):
        self.employee_id = employee_id
        self.employee_service = EmployeeService()
        self.order_service = OrderService()
        self.complaint_service = ComplaintService()
        self.report_service = ReportService()
        self.notification_service = NotificationService()
        self.menu = Menu("پنل کارمند")
        self.setup_menu()

    def setup_menu(self) -> None:
        self.menu.add_option("1", "مدیریت سفارش‌ها", self.manage_orders)
        self.menu.add_option("2", "مدیریت شکایات", self.manage_complaints)
        self.menu.add_option("3", "مشاهده گزارش‌ها", self.view_reports)
        self.menu.add_option("4", "خروج", self.exied)

    def show_menu(self) -> None:
        self.menu.display()

    def handle_menu_choice(self, choice: str) -> None:
        if choice in self.menu.options:
            _, action, _ = self.menu.options[choice]
            if action:
                action()


    def manage_orders(self) -> None:
        order_menu = Menu("مدیریت سفارش‌ها")
        order_menu.add_option("1", "مشاهده همه سفارش‌ها", self._list_all_orders)
        order_menu.add_option("2", "مشاهده سفارش‌های جدید", self._list_new_orders)
        order_menu.add_option("3", "مشاهده سفارش‌های در حال پردازش", self._list_processing_orders)
        order_menu.add_option("4", "مشاهده سفارش‌های تکمیل شده", self._list_completed_orders)
        order_menu.add_option("5", "بازگشت",None, self.menu)
        order_menu.execute()

    def manage_complaints(self) -> None:
        complaint_menu = Menu("مدیریت شکایات")
        complaint_menu.add_option("1", "مشاهده همه شکایات", self._list_all_complaints)
        complaint_menu.add_option("2", "مشاهده شکایات جدید", self._list_new_complaints)
        complaint_menu.add_option("3", "مشاهده شکایات در حال بررسی", self._list_processing_complaints)
        complaint_menu.add_option("4", "مشاهده شکایات حل شده", self._list_resolved_complaints)
        complaint_menu.add_option("5", "بازگشت",None, self.menu)
        complaint_menu.execute()

    def view_reports(self) -> None:
        report_menu = Menu("مشاهده گزارش‌ها")
        report_menu.add_option("1", "گزارش فروش", self._view_sales_report)
        report_menu.add_option("2", "گزارش محصولات", self._view_products_report)
        report_menu.add_option("3", "گزارش کاربران", self._view_users_report)
        report_menu.add_option("4", "گزارش شکایات", self._view_complaints_report)
        report_menu.add_option("5", "بازگشت",  None, self.menu)
        report_menu.execute()

    def _list_all_orders(self) -> None:
        orders = self.order_service.get_all_orders()
        if orders:
            for order in orders:
                print(
                    f"ID: {order['order_id']}, تاریخ: {order['order_date']}, مبلغ: {order['total_amount']}, وضعیت: {order['status']}")
        else:
            print("هیچ سفارشی یافت نشد.")

    def _list_new_orders(self) -> None:
        orders = self.order_service.get_orders_by_status("new")
        if orders:
            for order in orders:
                print(f"ID: {order['order_id']}, تاریخ: {order['order_date']},"
                      f" مبلغ: {order['total_amount']}, وضعیت: {order['status']}")

        else:
            print("هیچ سفارش جدیدی یافت نشد.")

    def _list_processing_orders(self) -> None:
        orders = self.order_service.get_orders_by_status("pending")
        if orders:
            for order in orders:
                print(f"ID: {order['order_id']}, تاریخ: {order['order_date']}, "
                      f"مبلغ: {order['total_amount']}, وضعیت: {order['status']}")

        else:
            print("هیچ سفارش در حال پردازشی یافت نشد.")

    def _list_completed_orders(self) -> None:
        orders = self.order_service.get_orders_by_status("paid")
        if orders:
            for order in orders:
                print(f"ID: {order['order_id']}, تاریخ: {order['order_date']},"
                      f" مبلغ: {order['total_amount']}, وضعیت: {order['status']}")

        else:
            print("هیچ سفارش تکمیل شده‌ای یافت نشد.")

    def _list_all_complaints(self) -> None:
        complaints = self.complaint_service.get_all_complaints()
        if complaints:
            for complaint in complaints:
                print(f"ID: {complaint['id']}, تاریخ: {complaint['date']}, وضعیت: {complaint['status']}")
        else:
            print("هیچ شکایتی یافت نشد.")

    def _list_new_complaints(self) -> None:
        complaints = self.complaint_service.get_complaints_by_status("new")
        if complaints:
            for complaint in complaints:
                print(f"ID: {complaint['id']}, تاریخ: {complaint['date']}, وضعیت: {complaint['status']}")
        else:
            print("هیچ شکایت جدیدی یافت نشد.")

    def _list_processing_complaints(self) -> None:
        complaints = self.complaint_service.get_complaints_by_status("processing")
        if complaints:
            for complaint in complaints:
                print(f"ID: {complaint['id']}, تاریخ: {complaint['date']}, وضعیت: {complaint['status']}")
        else:
            print("هیچ شکایت در حال بررسی یافت نشد.")

    def _list_resolved_complaints(self) -> None:
        complaints = self.complaint_service.get_complaints_by_status("resolved")
        if complaints:
            for complaint in complaints:
                print(f"ID: {complaint['id']}, تاریخ: {complaint['date']}, وضعیت: {complaint['status']}")
        else:
            print("هیچ شکایت حل شده‌ای یافت نشد.")

    def _view_sales_report(self) -> None:
        product_id = int(input("لطفا شناسه کالا را وارد نمایید"))
        data = self.report_service.get_sales_report(product_id)
        self.report_service.export_sales_to_excel(data)

    def _view_products_report(self) -> None:
        report = self.product
        if report:
            print("\n=== گزارش محصولات ===")
            print(f"تعداد کل محصولات: {report['total_products']}")
            print(f"تعداد محصولات فعال: {report['active_products']}")
            print(f"محصولات پرفروش: {report['popular_products']}")
        else:
            print("خطا در دریافت گزارش محصولات")

    def _view_users_report(self) -> None:
        report = self.report_service.get_users_report()
        if report:
            print("\n=== گزارش کاربران ===")
            print(f"تعداد کل کاربران: {report['total_users']}")
            print(f"تعداد مشتریان: {report['total_customers']}")
            print(f"تعداد فروشندگان: {report['total_sellers']}")
        else:
            print("خطا در دریافت گزارش کاربران")

    def _view_complaints_report(self) -> None:
        report = self.report_service.get_complaints_report()
        if report:
            print("\n=== گزارش شکایات ===")
            print(f"تعداد کل شکایات: {report['total_complaints']}")
            print(f"شکایات حل شده: {report['resolved_complaints']}")
            print(f"شکایات در حال بررسی: {report['processing_complaints']}")
        else:
            print("خطا در دریافت گزارش شکایات")
    def exied(self):
        exit("exit")
