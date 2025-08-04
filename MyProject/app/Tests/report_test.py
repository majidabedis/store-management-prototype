from Database.db.connection_manager import DatabaseManager
from typing import Dict, List, Optional

database_manager = DatabaseManager()
database_manager.connect()


def get_category_prefix(product_id: int) -> Optional[int]:
    return product_id // 1_000_000


# carts = DatabaseManager.generic_sql_fetch(
#     table="carts",
#     columns=[
#         "customer.name AS user_name",
#         "laptops.name AS product_name",
#         "cart_items.quantity",
#         "warehouse_stock.sale_price",
#         "warehouse_stock.seller_id",
#         "seller.name AS seller_name",
#         "(cart_items.quantity * warehouse_stock.sale_price) AS total_price"
#     ],
#     joins=[
#         ("customer", "carts.customer_id = customer.customer_id"),
#         ("cart_items", "carts.cart_id = cart_items.cart_id"),
#         ("laptops", "cart_items.product_id = laptops.laptop_id"),
#         ("warehouse_stock", "cart_items.product_id = warehouse_stock.product_id"),
#         ("seller", "warehouse_stock.seller_id = seller.seller_id "),
#
#     ],
#     filters=["warehouse_stock.stock_id = cart_items.stock_id"]
# )
# if len(carts) == 0:
#     print("no cart")
# else:
#     print(carts)

product_id = 97000001
prefix = get_category_prefix(product_id)
table = ""
category = ""
if prefix == 96:
    table = "cameras"
    category = "camera"
elif prefix == 97:
    table = "laptops"
    category = "laptop"
elif prefix == 98:
    table = "mobiles"
    category = "mobile"
data = DatabaseManager.generic_sql_fetch(
            table="invoices",
            columns=[
                "invoices.invoice_id AS invoice_number",
                "invoices.invoice_date AS invoice_date",
                "orders.order_id AS order_number",
                "customer.name AS customer_name",
                "order_items.seller_id,"
                "orders.order_id",
                "seller.name AS seller_name",
                f"{table}.name AS product_name",
                "invoices.paid_amount As paid_amount",
                "invoices.total_item As total_item",

                "invoices.payment_method As payment_method",
            ],
            joins=[
                ("customer", "invoices.customer_id = customer.customer_id"),
                ("orders", "orders.order_id = invoices.order_id"),
                ("order_items", "orders.order_id =order_items.order_id "),
                ("seller", "seller.seller_id = order_items.seller_id"),
                (f"{table}", f"{table}.{category}_id = order_items.product_id"),
            ],
            filters=[f"order_items.product_id = {product_id}"]
        )
print(data)

# invoice = DatabaseManager.generic_sql_fetch(
#     table="invoices",
#     columns=[
#         "invoices.invoice_id AS invoice_number",
#         "invoices.invoice_date AS invoice_date",
#         "orders.order_id AS order_number",
#         "customer.name AS customer_name",
#         "order_items.seller_id,"
#         "orders.order_id",
#         "seller.name AS seller_name",
#         f"{table}.name AS product_name",
#         "invoices.paid_amount As paid_amount",
#         "invoices.total_item As total_item",
#
#         "invoices.payment_method As payment_method",
#     ],
#     joins=[
#         ("customer", "invoices.customer_id = customer.customer_id"),
#         ("orders", "orders.order_id = invoices.order_id"),
#         ("order_items", "orders.order_id =order_items.order_id "),
#         ("seller", "seller.seller_id = order_items.seller_id"),
#         (f"{table}", f"{table}.{category}_id = order_items.product_id"),
#     ],
#     filters=["invoices.customer_id = customer.customer_id"],
# )
# if len(invoice) == 0:
#     print("no cart")
# else:
#     invoice = invoice[0]
#     print(f"شماره فاکتور: {invoice.get('invoice_number')}")
#     print(f"تاریخ فاکتور: {invoice.get('invoice_date')}")
#     print(f" اسم مشتری: {invoice.get('customer_name')}")
#     print(f" اسم فروشنده: {invoice.get('seller_name')}")
#     print(f" اسم کالا: {invoice.get('product_name')}")
#     print(f"تعداد کالا : {invoice.get('total_item')}")
#     print(f"روش پرداخت: {invoice.get('payment_method')}")
#     print(f"جمع کل: {invoice.get('paid_amount')}")


