# from Domains.users import BaseUser
# from datetime import datetime
#
#
# class Seller(BaseUser):
#     def __init__(self):
#         super().__init__()
#         self._shop_name = "Shop"
#         self._register_date = datetime.now().strftime("%Y-%m-%d")
#         self._position = "seller"
#         self._business_license = None
#         self._tax_number = None
#         self._bank_account = None
#         self._products = []
#         self._rating = 0.0
#         self._total_sales = 0.0
#
#     @property
#     def shop_name(self):
#         return self._shop_name
#
#     @shop_name.setter
#     def shop_name(self, value):
#         self._shop_name = self._validate_shop_name(value)
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
#     def business_license(self):
#         return self._business_license
#
#     @business_license.setter
#     def business_license(self, value):
#         self._business_license = self._validate_business_license(value)
#
#     @property
#     def tax_number(self):
#         return self._tax_number
#
#     @tax_number.setter
#     def tax_number(self, value):
#         self._tax_number = self._validate_tax_number(value)
#
#     @property
#     def bank_account(self):
#         return self._bank_account
#
#     @bank_account.setter
#     def bank_account(self, value):
#         self._bank_account = self._validate_bank_account(value)
#
#     @property
#     def products(self):
#         return self._products
#
#     @property
#     def rating(self):
#         return self._rating
#
#     @property
#     def total_sales(self):
#         return self._total_sales
#
#     def add_product(self, product):
#         if product not in self._products:
#             self._products.append(product)
#
#     def remove_product(self, product):
#         if product in self._products:
#             self._products.remove(product)
#
#     def update_product(self, old_product, new_product):
#         if old_product in self._products:
#             index = self._products.index(old_product)
#             self._products[index] = new_product
#
#     def get_sales_report(self, start_date=None, end_date=None):
#         # این متد باید با سیستم گزارش‌گیری پیاده‌سازی شود
#         return {
#             "total_sales": self._total_sales,
#             "number_of_orders": len(self._products),
#             "average_rating": self._rating
#         }
#
#     def update_rating(self, new_rating):
#         if 0 <= new_rating <= 5:
#             self._rating = new_rating
#         else:
#             raise ValueError("امتیاز باید بین 0 تا 5 باشد")
#
#     def to_dict(self):
#         base = super().to_dict()
#         base.update({
#             "shop_name": self.shop_name,
#             "register_date": self.register_date,
#             "position": self.position,
#             "business_license": self.business_license,
#             "tax_number": self.tax_number,
#             "bank_account": self.bank_account,
#             "rating": self.rating,
#             "total_sales": self.total_sales,
#             "products_count": len(self.products)
#         })
#         return base