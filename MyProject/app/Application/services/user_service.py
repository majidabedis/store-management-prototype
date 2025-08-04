from typing import List, Dict, Optional
import bcrypt
from Domains.users.base_user import User, Customer, Employee, Seller
from Database.repositories.user_repository import UserRepository
import json


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self._customer = Customer()
        self._seller = Seller()
        self._employee = Employee()



    def login_user(self, username: str, password: str) -> dict | None:
        try:
            users = self.get_all_users()
            for user in users:
                if user["username"] == username:
                    if user["status"] != "active":
                        print("اکانت شما غیر فعال میباشد ، لطفا با پشتیبانی تماس بگیرید")
                        return
                    else:
                        hashed_password = user["password"].encode("utf-8")
                        if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
                            return user
            print("نام کاربری یا رمز عبور اشتباه است")
            return None
        except Exception as e:
            print(f"خطا در ورود کاربر: {e}")
            return None

    def create_user(self, position: str, data: tuple) -> Optional[int]:
        try:
            user_data = self._prepare_user_data(position, data)
            if not user_data:
                return None
            raw_password = user_data.get("password")
            if raw_password:
                hashed = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
                user_data["password"] = hashed.decode('utf-8')

            for key in ['favorite_sellers', 'order_history', 'addresses', 'attendance_records']:
                if key in user_data:
                    user_data[key] = json.dumps(user_data.get(key, []))
            user_id = self.user_repository.add_person(user_data)
            return user_id

        except Exception as e:
            print(f"خطا در ایجاد کاربر: {e}")
            return None

    def _prepare_user_data(self, position: str, data: tuple) -> Optional[Dict]:
        try:
            if position == "customer":
                return self._prepare_customer_data(data)
            elif position == "seller":
                return self._prepare_seller_data(data)
            elif position == "employee":
                return self._prepare_employee_data(data)
            else:
                print("نوع کاربر معتبر نیست")
                return None
        except Exception as e:
            print(f"خطا در آماده‌سازی داده‌های کاربر: {e}")
            return None

    def _prepare_customer_data(self, data: tuple) -> Dict:
        customer = self._customer
        (
            customer.name, customer.family, customer.email, customer.password, customer.mobile,
            customer.birthday, customer.address, customer.city, customer.gender
        ) = data
        customer.username = customer.email
        customer.status = customer.STATUS_ACTIVE
        customer.position = "customer"
        return customer.to_dict()

    def _prepare_seller_data(self, data: tuple) -> Dict:
        seller = self._seller
        (
            seller.name, seller.family, seller.email, seller.password, seller.mobile,
            seller.birthday, seller.address, seller.city, seller.shop_name, seller.business_license,
            seller.tax_number, seller.gender
        ) = data
        seller.username = seller.email
        seller.status = seller.STATUS_PENDING
        seller.position = "seller"
        return seller.to_dict()

    def _prepare_employee_data(self, data: tuple) -> Dict:
        employee = self._employee
        (
            employee.name, employee.family, employee.email, employee.password, employee.mobile,
            employee.birthday, employee.address, employee.city, employee.gender, employee.department, employee.salary,
            employee.branch, employee.position
        ) = data
        employee.username = employee.email
        employee.status = employee.STATUS_ACTIVE
        return employee.to_dict()

    def get_all_users(self) -> List[Dict]:
        try:
            users = []
            for position in ["customer", "seller", "employee"]:
                position_users = self.user_repository.get_person(position)
                if position_users:
                    users.extend(position_users)
            for user in users:
                for key in ['favorite_sellers', 'order_history', 'addresses', 'products', 'attendance_records']:
                    if key in user and isinstance(user[key], str):
                        try:
                            user[key] = json.loads(user[key])
                        except json.JSONDecodeError:
                            user[key] = []
            return users
        except Exception as e:
            print(f"خطا در دریافت لیست کاربران: {e}")
            return []

    def search_users(self, search_term: str) -> List[Dict]:
        matched_users = []
        users = self.get_all_users()
        for user in users:
            name = user.get("name", "").lower()
            email = user.get("email", "").lower()
            if search_term.lower() in name or search_term.lower() in email:
                for key in ['favorite_sellers', 'order_history', 'cart', 'addresses', 'products', 'attendance_records']:
                    if key in user and isinstance(user[key], str):
                        try:
                            user[key] = json.loads(user[key])
                        except json.JSONDecodeError:
                            user[key] = []
                matched_users.append(user)
        return matched_users

    def get_category_prefix(self, user_id: int) -> Optional[int]:
        return user_id // 1_000_000

    def get_user_by_id(self, user_id: int, position: str) -> Optional[Dict]:
        try:
            prefix = self.get_category_prefix(user_id)
            print(prefix)
            if prefix == 20:
                position = "customer"
            elif prefix == 50:
                position = "employee"
            elif prefix == 60:
                position = "seller"
            else:
                raise ValueError("Invalid product ID prefix.")
            users = self.user_repository.get_person(position, f"{position}_id = {user_id}")
            if users:
                user = users[0]
                for key in ['favorite_sellers', 'order_history', 'cart', 'addresses', 'products', 'attendance_records']:
                    if key in user and isinstance(user[key], str):
                        try:
                            user[key] = json.loads(user[key])
                        except json.JSONDecodeError:
                            user[key] = []
                return user
            return None
        except Exception as e:
            print(f"خطا در دریافت کاربر: {e}")
            return None

    def get_user_by_filter(self, position: str, condition: str = None) -> List[Dict]:
        try:
            users = self.user_repository.get_person(position, condition)
            if not users:
                return []
            for user in users:
                for key in ['favorite_sellers', 'order_history', 'cart', 'addresses', 'products', 'attendance_records']:
                    if key in user and isinstance(user[key], str):
                        try:
                            user[key] = json.loads(user[key])
                        except json.JSONDecodeError:
                            user[key] = []

            return users
        except Exception as e:
            print(f"خطا در دریافت کاربران: {e}")
            return []

    def update_user(self, position: str, user_id: int, updates: Dict) -> bool:
        try:
            user = self.get_user_by_id(user_id, position)
            if not user:
                print("کاربری با این شناسه یافت نشد.")
                return False

            condition = f"{position}_id = {user_id}"

            domain_map = {
                "customer": Customer,
                "seller": Seller,
                "employee": Employee
            }

            if position not in domain_map:
                print("نوع کاربر نامعتبر است.")
                return False

            domain_class = domain_map[position]
            domain_instance = domain_class()

            updated_data = user.copy()
            updated_data.update(updates)
            readonly_fields = ['favorite_sellers', 'register_date','hire_date', 'order_history', 'addresses', 'products',
                               'attendance_records', 'business_license', 'tax_number', 'age','rating' ,'total_sales']
            for field in readonly_fields:
                updated_data.pop(field, None)

            for key, value in updated_data.items():
                if hasattr(domain_instance, key):
                    try:
                        setattr(domain_instance, key, value)
                    except Exception as e:
                        print(f"خطا در اعتبارسنجی فیلد '{key}': {e}")
                        return False

            validated_data = domain_instance.to_dict()
            print(validated_data)

            for key, value in validated_data.items():
                if isinstance(value, list) or isinstance(value, dict):
                    validated_data[key] = json.dumps(value)

            validated_data.pop(f'{position}_id', None)
            validated_data.pop('position', None)

            return self.user_repository.update_person(position, validated_data, condition)

        except Exception as e:
            print(f"خطا در به‌روزرسانی کاربر: {e}")
            return False

    def delete_user(self, position: str, user_id: int) -> bool:
        try:
            prefix = self.get_category_prefix(user_id)
            print(prefix)
            if prefix == 20:
                position = "customer"
            elif prefix == 50:
                position = "employee"
            elif prefix == 60:
                position = "seller"
            else:
                raise ValueError("Invalid product ID prefix.")
            user = self.get_user_by_id(user_id, position)
            if not user:
                print("کاربری با این شناسه یافت نشد.")
                return False

            condition = f"{position}_id = {user_id}"
            return self.user_repository.delete_person(position, condition)
        except Exception as e:
            print(f"خطا در حذف کاربر: {e}")
            return False

    def get_users_by_position(self, position: str) -> List[Dict]:
        try:
            if position not in ["customer", "seller", "employee"]:
                print("نوع کاربر نامعتبر است.")
                return []

            result = self.user_repository.get_person(position)
            if result is None:
                print(f"خطا در دریافت {position}ها از پایگاه داده.")
                return []

            return result
        except Exception as e:
            print(f"خطا در دریافت کاربران: {e}")
            return []


class AdminService(UserService):
    def __init__(self):
        super().__init__()

    def add_employee(self, info) -> None:
        employee_id = self.create_user("employee", info)
        if employee_id:
            print(f"کاربر با شناسه {employee_id} با موفقیت ثبت شد.")
        else:
            print("خطا در ثبت کاربر.")


class CustomerService(UserService):
    def __init__(self):
        super().__init__()

    def update_cart(self, user_id: int, position: str, cart_items: List[Dict]) -> bool:
        condition = f"{position}_id = {user_id}"

        cart_json = json.dumps(cart_items)

        updates = {"cart": cart_json}
        return self.user_repository.update_person(position, updates, condition)


class EmployeeService(UserService):
    def __init__(self):
        super().__init__()

    pass


class SellerService(UserService):
    def __init__(self):
        super().__init__()

    pass
