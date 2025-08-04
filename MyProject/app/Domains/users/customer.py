# from Domains.users import User
# from datetime import datetime
#
#
# class Customer(BaseUser):
#     def __init__(self):
#         super().__init__()
#         self._register_date = datetime.now().strftime("%Y-%m-%d")
#         self._position = "customer"
#         self._digital_wallet = 0.0
#         self._loyalty_points = 0
#         self._favorite_sellers = []
#         self._order_history = []
#         self._cart = []
#         self._addresses = []
#
#     @property
#     def register_date(self):
#         return self._register_date
#
#     @register_date.setter
#     def register_date(self, value):
#         self._register_date = self._validate_register_date(value)
#
#     @property
#     def position(self):
#         return self._position
#
#     @position.setter
#     def position(self, value):
#         self._position = self._validate_position(value)
#
#     @property
#     def digital_wallet(self):
#         return self._digital_wallet
#
#     @digital_wallet.setter
#     def digital_wallet(self, value):
#         self._digital_wallet = self._validate_digital_wallet(value)
#
#     @property
#     def loyalty_points(self):
#         return self._loyalty_points
#
#     @loyalty_points.setter
#     def loyalty_points(self, value):
#         self._loyalty_points = self._validate_loyalty_points(value)
#
#     @property
#     def favorite_sellers(self):
#         return self._favorite_sellers
#
#     @property
#     def order_history(self):
#         return self._order_history
#
#     @property
#     def cart(self):
#         return self._cart
#
#     @property
#     def addresses(self):
#         return self._addresses
#
#     def add_to_cart(self, product):
#         if product not in self._cart:
#             self._cart.append(product)
#
#     def remove_from_cart(self, product):
#         if product in self._cart:
#             self._cart.remove(product)
#
#     def checkout(self):
#         if not self._cart:
#             raise ValueError("سبد خرید خالی است")
#
#         # اینجا منطق پرداخت و ثبت سفارش پیاده‌سازی می‌شود
#         order = {
#             "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "items": self._cart.copy(),
#             "status": "pending"
#         }
#         self._order_history.append(order)
#         self._cart.clear()
#
#     def add_address(self, address):
#         if address not in self._addresses:
#             self._addresses.append(address)
#
#     def set_default_address(self, address):
#         if address in self._addresses:
#             self._addresses.remove(address)
#             self._addresses.insert(0, address)
#
#     def add_favorite_seller(self, seller):
#         if seller not in self._favorite_sellers:
#             self._favorite_sellers.append(seller)
#
#     def remove_favorite_seller(self, seller):
#         if seller in self._favorite_sellers:
#             self._favorite_sellers.remove(seller)
#
#     def add_points(self, points):
#         self.loyalty_points += points
#
#     def redeem_points(self, points):
#         if points > self.loyalty_points:
#             raise ValueError("امتیاز کافی نیست")
#         self.loyalty_points -= points
#
#     def to_dict(self):
#         base = super().to_dict()
#         base.update({
#             "loyalty_points": self.loyalty_points,
#             "register_date": self.register_date,
#             "position": self.position,
#             "digital_wallet": self.digital_wallet,
#             "favorite_sellers_count": len(self.favorite_sellers),
#             "order_history_count": len(self.order_history),
#             "cart_count": len(self.cart),
#             "addresses_count": len(self.addresses)
#         })
#         return base
#
