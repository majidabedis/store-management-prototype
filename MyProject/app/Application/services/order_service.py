from typing import Dict, List, Optional
import jdatetime
from Database.repositories.order_item_repository import OrderItemRepository
from Database.repositories.order_repository import OrderRepository
from Database.repositories.product_repository import ProductRepository
from Application.services.cart_service import CartService
from Application.services.paid_service import PaidService


class OrderService:
    def __init__(self):
        self.order_repository = OrderRepository()
        self.order_item_repository = OrderItemRepository()
        self.product_repository = ProductRepository()
        self.cart_service = CartService()
        self.paid_service = PaidService()

    def get_all_orders(self) -> List[Dict]:
        return self.order_repository.get_all()

    def get_seller_orders(self, stock_id) -> List[Dict]:
        return self.order_item_repository.get_seller_orders(stock_id)

    def get_order_by_id(self, order_id: int) -> Optional[Dict]:
        return self.order_repository.get_by_id(order_id)

    def get_order_items_by_order_id(self, order_id: int) -> dict | None:
        return self.order_item_repository.get_by_id(order_id)

    def create_order(self, user_id: int, ) -> Optional[int]:
        cart = self.cart_service.get_carts(user_id)
        cart_items = self.cart_service.get_cart(user_id)
        cart_id = cart.get('cart_id')
        stock_id = cart_items[0].get('stock_id')
        if not cart or not cart_items:
            print("سبد خرید خالی میباشد شما به قسمت سفارش ها منتقل میشوید")
            return False
        total_items = len(cart_items)
        total_amount = 0
        for item in cart_items:
            total_amount += item['sale_price'] * item['quantity']

        order = {
            "customer_id": user_id,
            "cart_id": cart_id,
            "total_items": total_items,
            "total_amount": total_amount,
            "status": "pending"
        }
        order_id = self.order_repository.add(order)
        for product in cart_items:
            order_item = {
                "order_id": order_id,
                "product_id": product.get('product_id'),
                "stock_id": stock_id,
                "quantity": product.get('quantity'),
                "price": product.get('sale_price'),
            }
            self.order_item_repository.add(order_item)
            self.cart_service.remove_item(cart_id)

    def update_order_status(self, order_id: int, status: str) -> bool:
        valid_statuses = ['pending', 'paid', 'shipping', 'delivered', 'cancelled']
        if status not in valid_statuses:
            return False
        return self.order_repository.update(order_id, {'status': status})

    def cancel_order(self, order_id: int, user_id: int) -> bool:
        order = self.order_repository.get_by_id(order_id)
        if not order or order['user_id'] != user_id:
            return False
        return self.update_order_status(order_id, 'cancelled')

    def get_user_orders(self, user_id: int) -> List[Dict]:
        return self.order_repository.get_by_user_id(user_id)

    def get_orders_by_status(self, status: str) -> List[Dict]:
        return self.order_repository.get_by_status(status)

    # def process_order(self, order_id: int) -> bool:
    #     order = self.order_repository.get_by_id(order_id)
    #     if not order or order['status'] != 'pending':
    #         return False
    #
    #     for item in order['items']:
    #         product = self.product_repository.get_by_id(item['product_id'])
    #         if not product or product['stock'] < item['quantity']:
    #             return False
    #         self.product_repository.update(
    #             item['product_id'],
    #             {'stock': product['stock'] - item['quantity']}
    #         )
    #
    #     return self.update_order_status(order_id, 'paid')
