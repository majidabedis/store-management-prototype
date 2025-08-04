from typing import Dict, List, Optional
from datetime import datetime, timedelta
from Database.repositories.order_repository import OrderRepository
from Database.repositories.product_repository import ProductRepository
from Database.repositories.user_repository import UserRepository
from Database.repositories.complaint_repository import ComplaintRepository
from Database.repositories.report_repository import ReportRepository
from openpyxl import Workbook


class ReportService:
    def __init__(self):
        self.order_repository = OrderRepository()
        self.product_repository = ProductRepository()
        self.user_repository = UserRepository()
        self.complaint_repository = ComplaintRepository()
        self.report_repository = ReportRepository()

    def get_sales_report(self, product_id) -> List[Dict]:
        data = self.report_repository.create_report(
            table="invoice",
            columns=[
                "invoice.invoice_id AS invoice_number",
                "invoice.invoice_date AS invoice_date",
                "orders.order_id AS order_number",
                "customer.name AS customer_name",
                "seller.name AS seller_name",
                "product.name AS product_name",
                "product.product_id",
                "invoice.paid_amount AS paid_amount",
                "invoice.total_item AS total_item",
                "invoice.payment_method AS payment_method",
            ],
            joins=[
                ("customer", "invoice.customer_id = customer.customer_id"),
                ("orders", "invoice.order_id = orders.order_id"),
                ("order_item", "orders.order_id = order_item.order_id"),
                ("product", "product.product_id = order_item.product_id"),
                ("stock", "order_item.stock_id = stock.stock_id"),
                ("seller", "stock.seller_id = seller.seller_id"),
            ],
            filters=[f"order_item.product_id = {product_id}"]
        )
        if not data:
            print("هیچ گزارشی برای این محصول یافت نشد.")
            return []

        print(f"📊 تعداد کل فروش این محصول: {len(data)}\n")

        for idx, invoice in enumerate(data, start=1):
            print(f"{idx}. فاکتور:")
            print(f"شماره فاکتور: {invoice.get('invoice_number')}")
            print(f"تاریخ فاکتور: {invoice.get('invoice_date')}")
            print(f"شماره سفارش: {invoice.get('order_number')}")
            print(f"اسم مشتری: {invoice.get('customer_name')}")
            print(f"نام کالا: {invoice.get('product_name')}")
            print(f"تعداد کالا: {invoice.get('total_item')}")
            print(f"روش پرداخت: {invoice.get('payment_method')}")
            print(f"جمع کل: {invoice.get('paid_amount')}")
            print("-" * 40)

        return data

    def export_sales_to_excel(self, data: list, file_name: str = "sales_report.xlsx"):
        if not data:
            print("هیچ داده‌ای برای ذخیره در اکسل وجود ندارد.")
            return
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Sales Report"
        headers = list(data[0].keys())
        sheet.append(headers)
        for row in data:
            sheet.append([self.format_value(row.get(col)) for col in headers])

        workbook.save(file_name)
        print(f"✅ فایل گزارش با موفقیت در {file_name} ذخیره شد.")

    def get_product_performance_report(self, product_id: Optional[int] = None) -> List[Dict]:
        pass

    def get_customer_report(self, customer_id: Optional[int] = None) -> List[Dict]:
        pass

    def get_seller_report(self, seller_id: Optional[int] = None) -> List[Dict]:
        pass

    def get_complaint_report(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> Dict:
        pass

    @staticmethod
    def format_value(value):
        if hasattr(value, 'strftime'):
            return value.strftime('%Y/%m/%d')
        return str(value)
