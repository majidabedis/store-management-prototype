from typing import List, Dict, Optional
from Domains.products.base_product import Product, Mobile, Camera, Laptop
from Database.repositories.product_repository import ProductRepository
import json


class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()
        self._camera = Camera()
        self._laptop = Laptop()
        self._mobile = Mobile()

    def create_product(self, data: tuple) -> Optional[int]:
        """
       create product with given data
        :param data:  tuple
        :return: product id or None
        """
        try:
            category = data[3]
            product_data = self._prepare_product_data(category, data)
            if not product_data:
                return None

            product_data['images'] = json.dumps(product_data.get('images', []))
            product_data['product_spect'] = json.dumps(product_data.get('product_spect', []))
            product_id = self.product_repository.add_product(product_data)
            return product_id
        except Exception as e:
            print(f"خطا در ایجاد محصول: {e}")
            return None

    def create_product_temp(self, data: tuple, seller_id: int) -> Optional[int]:
        """
       create product with given data
        :param data:  tuple
        :return: product id or None
        """
        try:
            category = data[3]
            product_data = self._prepare_product_data(category, data)
            if not product_data:
                return None
            product_data.update({'seller_id': seller_id})
            product_data['images'] = json.dumps(product_data.get('images', []))
            product_data['product_spect'] = json.dumps(product_data.get('product_spect', []))
            product_id = self.product_repository.add_product_temp(product_data)
            return product_id
        except Exception as e:
            print(f"خطا در ایجاد محصول: {e}")
            return None

    def _prepare_product_data(self, category: str, data: tuple) -> Optional[Dict]:
        try:
            if category == "camera":
                return self._prepare_camera_data(data)
            elif category == "mobile":
                return self._prepare_mobile_data(data)
            elif category == "laptop":
                return self._prepare_laptop_data(data)
            else:
                print("دسته‌بندی معتبر نیست")
                return None
        except Exception as e:
            print(f"خطا در آماده‌سازی داده‌های محصول: {e}")
            return None

    def _prepare_camera_data(self, data: tuple) -> Dict:
        camera = self._camera
        (
            camera.name, camera.description, camera.price, camera.category,
            camera.brand, camera.model, camera.markup, camera.warranty_months, camera.color, camera.sensor_type,
            camera.sensor_size, camera.resolution, camera.lens_type, camera.lens_mount,
            camera.iso_range, camera.shutter_speed, camera.video_resolution
        ) = data
        camera.status = camera.STATUS_ACTIVE
        return camera.to_dict()

    def _prepare_mobile_data(self, data: tuple) -> Dict:
        mobile = self._mobile
        (
            mobile.name, mobile.description, mobile.price, mobile.category,
            mobile.brand, mobile.model, mobile.markup, mobile.warranty_months, mobile.color,
            mobile.screen_size, mobile.ram, mobile.storage, mobile.battery_capacity,
            mobile.os, mobile.camera_resolution, mobile.processor
        ) = data
        mobile.status = mobile.STATUS_INACTIVE
        return mobile.to_dict()

    def _prepare_laptop_data(self, data: tuple) -> Dict:
        laptop = self._laptop
        (
            laptop.name, laptop.description, laptop.price, laptop.category,
            laptop.brand, laptop.model, laptop.warranty_months, laptop.color,
            laptop.screen_size, laptop.processor, laptop.ram, laptop.storage,
            laptop.graphics_card, laptop.battery_life, laptop.weight, laptop.os
        ) = data
        return laptop.to_dict()

    def get_all_products(self) -> List[Dict]:
        try:
            products = self.product_repository.read_product()
            return products
        except Exception as e:
            print(f"خطا در دریافت لیست محصولات: {e}")
            return []

    def get_product_by_id(self, product_id: int) -> list[dict] | None:
        condition = f"product_id = {product_id}"
        data = self.product_repository.read_product(condition)
        return data if data is not None else None

    def search_product(self, condition) -> List[Dict]:
        return self.product_repository.read_product(condition)

    def search_temp_product(self, condition) -> List[Dict]:
        return self.product_repository.read_product_temp(condition)

    def get_products_by_category(self, category: str) -> List[Dict]:
        try:
            if category not in ["camera", "mobile", "laptop"]:
                print("دسته‌بندی نامعتبر است.")
                return []

            return self.product_repository.read_product(category)
        except Exception as e:
            print(f"خطا در دریافت محصولات: {e}")
            return []

    def search_product_temp(self, condition) -> List[Dict]:
        return self.product_repository.read_product_temp(condition)

    def get_seller_products(self, seller_id) -> List[Dict]:
        condition = f"seller_id = {seller_id}"
        return self.product_repository.read_product_temp()

    def update_product(self, product_id: int, updates: Dict) -> bool:
        try:
            product = self.search_product(product_id)
            if not product:
                print("محصولی با این شناسه یافت نشد.")
                return False
            product = product[0]
            condition = f"product_id = {product_id}"
            updated_data = product.copy()
            updated_data.update(updates)
            readonly_fields = ['product_id', 'created_at', 'images', 'category', 'price']
            for field in readonly_fields:
                updated_data.pop(field, None)
            if 'images' in updated_data:
                updated_data['images'] = json.dumps(updated_data['images'])

            return self.product_repository.update_product(updated_data, condition)

        except Exception as e:
            print(f"خطا در به‌روزرسانی محصول: {e}")
            return False

    def update_product_temp(self, product_temp_id: int, updates: Dict) -> bool:
        try:
            product = self.search_product_temp(product_temp_id)
            if not product:
                print("محصولی با این شناسه یافت نشد.")
                return False
            product = product[0]
            condition = f"product_temp_id = {product_temp_id}"
            updated_data = product.copy()
            updated_data.update(updates)
            readonly_fields = ['product_temp_id', 'created_at', 'images', 'category', 'sale_price']
            for field in readonly_fields:
                updated_data.pop(field, None)

            if 'images' in updated_data:
                updated_data['images'] = json.dumps(updated_data['images'])

            return self.product_repository.update_product_temp(updated_data, condition)

        except Exception as e:
            print(f"خطا در به‌روزرسانی محصول: {e}")
            return False

    def delete_product(self, product_id: int) -> bool:
        try:
            product = self.get_product_by_id(product_id)
            if not product:
                print("محصولی با این شناسه یافت نشد.")
                return False
            product = product[0]
            category = product['category']
            condition = f"product_id = {product_id}"
            return self.product_repository.delete_product(condition)
        except Exception as e:
            print(f"خطا در حذف محصول: {e}")
            return False

    def delete_product_temp(self, product_temp_id: int) -> bool | None:
        try:
            condition = f"product_temp_id = {product_temp_id}"
            product = self.search_product_temp(condition)
            if not product:
                print("محصولی با این شناسه یافت نشد.")
                return False
            product = product[0]
            product_temp_id = product['product_temp_id']
            conditionn = f"product_temp_id = {product_temp_id}"
            self.product_repository.delete_product_temp(conditionn)

        except Exception as e:
            print(f"خطا در حذف محصول: {e}")
            return False
