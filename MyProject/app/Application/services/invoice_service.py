from typing import Dict, List, Optional
import jdatetime
from Database.repositories.invoice_repository import InvoiceRepository


class InvoiceService:
    def __init__(self):
        self.invoice_repository = InvoiceRepository()

    def create_invoice(self, user_id: int, order_id: int, paid_id: int, total_item: int,
                       paid_total: float) -> Optional[bool]:
        if user_id and order_id and paid_id:
            data = {
                "customer_id": user_id,
                "order_id": order_id,
                "paid_id": paid_id,
                "total_item": total_item,
                "total_amount": paid_total,
                "paid_amount": paid_total,
                "payment_method": "online",
                "status": "paid"
            }

            self.invoice_repository.add(data)

    def show_factor(self, product_id: int, order_id: int):
        invoice = self.invoice_repository.join(
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
            filters=[
                f"invoice.order_id = {order_id}",
                f"product.product_id = {product_id}"
            ],
        )
        if not invoice:
            print("no order")
            return
        invoice = invoice[0]
        print("-------------فاکتور خرید---------------")
        print("-" * 50)
        print(f"شماره فاکتور: {invoice.get('invoice_number')}")
        print(f"تاریخ فاکتور: {invoice.get('invoice_date')}")
        print(f"اسم مشتری: {invoice.get('customer_name')}")
        print(f"اسم فروشنده: {invoice.get('seller_name')}")
        print(f"شماره سفارش: {invoice.get('order_number')}")
        print(f"اسم کالا: {invoice.get('product_name')}")
        print(f"تعداد کالا : {invoice.get('total_item')}")
        print(f"روش پرداخت: {invoice.get('payment_method')}")
        print(f"جمع کل: {invoice.get('paid_amount')}")
        print("-" * 50)
