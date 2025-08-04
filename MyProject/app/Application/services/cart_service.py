from typing import Dict, List, Optional, Any
import jdatetime

from Database.repositories import cart_repository
from Database.repositories.cart_repository import CartRepository
from Database.repositories.cart_item_repository import Cart_Item_Repository
from Application.services.stock_service import StockService
from Application.services.user_service import CustomerService


class CartService:
    def __init__(self):
        self.cart_repository = CartRepository()
        self.cart_item_repository = Cart_Item_Repository()
        self.stock_service = StockService()
        self.customer_service = CustomerService()

    # **********create and add to cart**********
    def add_to_cart(self, user_id: int, product_id: int, quantity: int) -> bool | None:
        cart = self.cart_repository.get_by_id(user_id)
        if cart:
            cart_id = cart.get('cart_id') or cart.get('id')
            print("سبد خرید موجود است.")
        else:
            cart_data = {
                'customer_id': user_id,
                'created_at': jdatetime.date.today().strftime("%Y-%m-%d"),
            }
            cart_id = self.cart_repository.add(cart_data)
            print("سبد خرید جدید ساخته شد.")
            return cart_id

        available_stocks = self.cart_repository.join(
            table="stock",
            columns=[
                "stock.stock_id", "stock.product_id", "stock.quantity",
                "stock.sale_price", "stock.warehouse_id",
                "seller.seller_id", "seller.name AS seller_name"
            ],
            joins=[("seller", "stock.seller_id = seller.seller_id")],
            filters=[f"stock.product_id = {product_id}", "stock.quantity > 0"]
        )

        if not available_stocks:
            print("هیچ فروشنده‌ای برای این کالا موجود نیست.")
            return

        for idx, item in enumerate(available_stocks, start=1):
            print(f"{idx}. فروشنده: {item['seller_name']} | قیمت: {item['sale_price']} | موجودی: {item['quantity']}")

        try:
            choice = int(input("یکی از فروشنده‌ها را انتخاب کنید: "))
            selected_item = available_stocks[choice - 1]
        except (ValueError, IndexError):
            print("انتخاب نامعتبر بود.")
            return

        stock_id = int(selected_item["stock_id"])
        current_stock_quantity = selected_item["quantity"]

        if current_stock_quantity < quantity:
            print("مقدار درخواستی بیش از موجودی انبار است.")
            return False
        existing_cart_item = self.cart_item_repository.get_by_cart_stock_id(stock_id)

        if not existing_cart_item:
            cart_item_data = {
                "cart_id": cart_id,
                "product_id": selected_item["product_id"],
                "stock_id": stock_id,
                "quantity": quantity,
                "price": selected_item["sale_price"]
            }
            item_added = self.cart_item_repository.add(cart_item_data)

            if not item_added:
                print("افزودن آیتم به سبد خرید ناموفق بود.")
                return False

            print("آیتم جدید به سبد خرید افزوده شد.")

        else:
            cart_item_id = existing_cart_item["cart_item_id"]
            current_quantity = existing_cart_item["quantity"]
            new_quantity = current_quantity + quantity

            update_success = self.cart_item_repository.update_cart_item(
                cart_item_id, {"quantity": new_quantity}
            )

            if not update_success:
                print("خطا در افزایش تعداد کالا در سبد خرید.")
                return False

            print("تعداد کالا در سبد خرید افزایش یافت.")

        new_stock_quantity = current_stock_quantity - quantity
        stock_updated = self.stock_service.update_stock(
            stock_id=stock_id, updates={"quantity": new_stock_quantity}
        )

        if stock_updated:
            print("موجودی انبار به‌روزرسانی شد.")
            return True
        else:
            print("کاهش موجودی انبار با خطا مواجه شد.")
            return False

    # ******************search carts section*********************

    def get_cart_item(self, cart_item_id: int) -> Optional[Dict]:
        return self.cart_item_repository.get_by_cart_item_id(cart_item_id)

    def get_carts(self, user_id: int) -> Optional[Dict]:
        return self.cart_repository.get_by_id(user_id)

    def get_cart(self, user_id: int) -> list[Any] | None:
        cart = self.get_carts(user_id)
        if not cart:
            print("سبد خرید پیدا نشد.")
            return

        cart_id = cart.get('cart_id')
        cart_items = self.cart_item_repository.get_by_cart_id(cart_id)
        if not cart_items:
            print("سبد خرید خالی است.")
            return

        all_results = []

        for items in cart_items:
            product_id = items.get('product_id')
            results = self.cart_repository.join(
                table="cart",
                columns=[
                    "customer.name AS user_name",
                    "product.name AS product_name",
                    "product.product_id AS product_id",
                    "cart_item.quantity",
                    "cart_item.cart_item_id",
                    "stock.sale_price",
                    "stock.seller_id",
                    "stock.stock_id",
                    "stock.quantity AS stock_quantity",
                    "seller.name AS seller_name",
                    "(cart_item.quantity * stock.sale_price) AS total_price"
                ],
                joins=[
                    ("customer", "cart.customer_id = customer.customer_id"),
                    ("cart_item", "cart.cart_id = cart_item.cart_id"),
                    ("product", "cart_item.product_id = product.product_id"),
                    ("stock", "cart_item.stock_id = stock.stock_id"),
                    ("seller", "stock.seller_id = seller.seller_id"),
                ],
                filters=[
                    f"stock.stock_id = {items.get('stock_id')}",
                    f"cart_item.cart_item_id = {items.get('cart_item_id')}"
                ]
            )
            all_results.extend(results)
        self._get_cart_items_details(all_results)
        return all_results

    #remove cart item

    def remove_from_cart(self, user_id: int) -> bool | None:
        data = self.get_cart(user_id)
        for idx, item in enumerate(data, start=1):
            print(
                f"{idx}. شماره سفارش: {item['cart_item_id']} |نام کالا : {item['product_name']} | "
                f"قیمت: {item['sale_price']} |تعداد: {item['quantity']}")
        try:
            choice = int(input("سفارش مورد نظر را انتخاب کنید: "))
            selected_item = data[choice - 1]
            agree = input(f"آیا از حذف کالا مطمئن هستید؟ {selected_item['product_name']}  \n"
                          f"1.بله \n"
                          f"2.خیر ")

            if agree.strip() != "1":
                return False
            stock_id = selected_item["stock_id"]
            quantity_in_cart = selected_item["quantity"]
            current_stock_quantity = selected_item["stock_quantity"]

            new_stock_quantity = current_stock_quantity + quantity_in_cart
            self.stock_service.update_stock(stock_id, {"quantity": new_stock_quantity})

            self.cart_item_repository.clear_cart_item(selected_item["cart_item_id"])
            return True

        except (ValueError, IndexError):
            print("انتخاب نامعتبر بود.")
            return None

    # ****************** update cart ******************
    def update_cart_item(self, user_id, quantity, inc) -> bool | None:
        data = self.get_cart(user_id)
        for idx, item in enumerate(data, start=1):
            print(
                f"{idx}. شماره سفارش: {item['cart_item_id']} |نام کالا : {item['product_name']} | "
                f"قیمت: {item['sale_price']} |تعداد: {item['quantity']}")
        try:
            choice = int(input("سفارش مورد نظر را انتخاب کنید: "))
            selected_item = data[choice - 1]
        except (ValueError, IndexError):
            print("انتخاب نامعتبر بود.")
            return

        old_quantity = selected_item["quantity"]
        new_quantity = 0
        stock_change = 0

        if inc == "1":
            new_quantity = old_quantity + quantity
            stock_change = -quantity

        elif inc == "2":
            new_quantity = old_quantity - quantity
            stock_change = quantity

            if new_quantity <= 0:
                self.cart_item_repository.clear_cart_item(selected_item["cart_item_id"])
                self.stock_service.update_stock(
                    selected_item['stock_id'],
                    {"quantity": selected_item["stock_quantity"] + old_quantity}
                )
                return True

        update_quantity = {"quantity": new_quantity}
        update_warehouse = {"quantity": selected_item["stock_quantity"] + stock_change}
        result = self.cart_item_repository.update_cart_item(selected_item["cart_item_id"], update_quantity)
        self.stock_service.update_stock(selected_item['stock_id'], update_warehouse)
        return result if result else False

    def clear_cart(self, user_id: int) -> bool | None:
        cart = self.cart_repository.get_by_user_id(user_id)
        if not cart:
            return
        result = self.cart_repository.update(cart['cart_id'], {'items': []})
        return result if result else False

    def remove_item(self, cart_id: int) -> bool | None:
        self.cart_item_repository.remove(cart_id)

    def _get_cart_items_details(self, items: List[Dict]) -> None:
        for item in items:
            print("*" * 50)
            print(f'___________ شماره سفارش: {item['cart_item_id']} ____________'),
            print(f'شماره انبار: {item['stock_id']}'),
            print(f'موجودی انبار : {item['stock_quantity']}'),
            print(f'نام کاربری: {item['user_name']}'),
            print(f'نام کالا: {item['product_name']}'),
            print(f'قیمت: {item['sale_price']}'),
            print(f'تعداد: {item['quantity']}'),
            print(f'نام فروشنده: {item['seller_name']}'),
            print(f'جمع کل: {item['total_price']}')
            print("*" * 50)


