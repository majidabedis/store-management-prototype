from typing import Tuple, Any, Set, Dict
from utils.input_utils import get_common_fields, invalid_input, choose_from_valid_data, get_product_fields
from Application.services.user_service import UserService
from Application.services.product_service import ProductService
from Database.InfoData import valid_data


class Registration:
    def __init__(self):
        self.user_service = UserService()
        self.product_service = ProductService()
        self.valid_data = valid_data

    def register_customer(self) -> tuple[Any, str | None] | None:
        fields = get_common_fields()
        gender = choose_from_valid_data("gender", self.valid_data)
        data = (*fields, gender)
        if fields:
            return data
        return None

    def register_seller(self) -> tuple | None:
        fields = get_common_fields()
        gender = choose_from_valid_data("gender", self.valid_data)
        choice = input("1.بله  2.خیر  آیا فروشگاه/شرکت دارید؟ ")

        if choice == "1":
            shop_name = invalid_input("نام فروشگاه:", r'^[a-zA-Z\u0600-\u06FF]{2,}$', "نام فروشگاه نامعتبر است")
            business_license = invalid_input("شماره مجوز:", r'^\d{10}$', "شماره مجوز نامعتبر است")
            tax_number = invalid_input("شماره مالیاتی:", r'^\d{10}$', "شماره مالیاتی نامعتبر است")
        else:
            shop_name = "None"
            business_license = None
            tax_number = None

        data = (*fields, shop_name, business_license, tax_number, gender)
        if fields:
            return data
        return None

    def register_employee(self) -> tuple | None:
        fields = get_common_fields()
        gender = choose_from_valid_data("gender", self.valid_data)
        department = choose_from_valid_data("department", self.valid_data)
        salary = float(invalid_input("لطفا حقوق کارمند را تعیین نمایید", r'^\d{4,}$', "حقوق کارمند معتبر نمی باشد "))
        branch = choose_from_valid_data("branch", self.valid_data)
        position = choose_from_valid_data("position", self.valid_data)

        data = (*fields, gender, department, salary, branch, position)
        if fields:
            return data
        return None

    def register_product(self) -> tuple | None:
        category = choose_from_valid_data("category", self.valid_data)
        fields = get_product_fields()
        markup = choose_from_valid_data("markup", self.valid_data)
        warranty_months = choose_from_valid_data("warranty_months", self.valid_data)
        color = choose_from_valid_data("colors", self.valid_data)
        if category == "camera":
            brand = choose_from_valid_data("camera_brand", self.valid_data)
            model = choose_from_valid_data("camera_model", self.valid_data)
            sensor_type = choose_from_valid_data("sensor_type", self.valid_data)
            sensor_size = choose_from_valid_data("sensor_size", self.valid_data)
            resolution = choose_from_valid_data("resolution", self.valid_data)
            lens_type = choose_from_valid_data("lens_type", self.valid_data)
            lens_mount = choose_from_valid_data("lens_mount", self.valid_data)
            iso = choose_from_valid_data("iso", self.valid_data)
            shutter_speed = choose_from_valid_data("shutter_speed", self.valid_data)
            video_resolution = choose_from_valid_data("video_resolution", self.valid_data)
            full_data = (
                *fields, category, markup, warranty_months, color, brand, model, sensor_type, sensor_size,
                resolution, lens_mount, lens_type, iso, shutter_speed, video_resolution)
            if full_data:
                return full_data
        elif category == "mobile":
            brand = choose_from_valid_data("mobile_brand", self.valid_data)
            model = choose_from_valid_data("mobile_model", self.valid_data)
            screen_size = choose_from_valid_data("resolution", self.valid_data)
            ram = choose_from_valid_data("ram", self.valid_data)
            storage = choose_from_valid_data("storage", self.valid_data)
            battery_capacity = choose_from_valid_data("battery_capacity", self.valid_data)
            os = choose_from_valid_data("os", self.valid_data)
            camera_resolution = choose_from_valid_data("camera_resolution", self.valid_data)
            processor = choose_from_valid_data("processor", self.valid_data)
            full_data = (*fields, category, brand, model, markup, warranty_months, color,
                         screen_size, ram, storage, battery_capacity, os, camera_resolution, processor)
            if full_data:
                return full_data
        elif category == "laptop":
            brand = choose_from_valid_data("laptop_brand", self.valid_data)
            model = choose_from_valid_data("laptop_model", self.valid_data)
            screen_size = choose_from_valid_data("screen_size", self.valid_data)
            processor = choose_from_valid_data("processor", self.valid_data)
            ram = choose_from_valid_data("ram", self.valid_data)
            storage = choose_from_valid_data("storage", self.valid_data)
            graphics_card = choose_from_valid_data("graphics_card", self.valid_data)
            battery_life = choose_from_valid_data("battery_life", self.valid_data)
            weight = choose_from_valid_data("weight", self.valid_data)
            os = choose_from_valid_data("os", self.valid_data)
            full_data = (*fields, category, brand, model, warranty_months, color,
                         screen_size, processor, ram, storage, graphics_card, battery_life, weight, os)
            if full_data:
                return full_data

    def register_warehouse(self) -> dict[str, str | None | int] | None:
        name = invalid_input("نام انبار را وارد نمایید", r'^[a-zA-Z\u0600-\u06FF]{2,}$', "نام انبار معتبر نیست ")
        location = invalid_input("لطفا ادرس انبار را وارد نمایید", r'^[a-zA-Z\u0600-\u06FF]{2,}$', "آدرس معتبر نیست")
        warehouse_type = choose_from_valid_data("warehouse_type", self.valid_data)
        branch_name = choose_from_valid_data("branch", self.valid_data)
        #

        data = {
            "name": name,
            "location": location,
            "warehouse_type": warehouse_type,
            "branch_name": branch_name
        }

        if data:
            return data
        else:
            return None

    def add_stock(self) ->dict | None:
        warehouse_id = invalid_input("آیدی انبار را وارد نمایید", r'^\d{1,}$', "آیدی انبار معتبر نیست")
        product_id = invalid_input("لطفا آِدی کالا مورد نظر را وارد نمایید", r'^\d{1,}$', "آیدی کالا معتبر نیست ")
        seller_id = invalid_input("آیدی فروشنده را وارد نمایید", r'^\d{1,}$', "آیدی فروشنده معتبر نیست")
        quantity = int(invalid_input("تعداد کالا را وارد نمایید ", r'^\d{1,}$', "تعداد معتبر نیست"))
        markup = choose_from_valid_data("markup", self.valid_data)
        discount = choose_from_valid_data("discount", self.valid_data)
        data = {
            "warehouse_id": warehouse_id,
            "product_id": product_id,
            "seller_id": seller_id,
            "quantity": quantity,
            "markup": markup,
            "discount": discount
        }
        if data:
            return data
        else:
            return None
