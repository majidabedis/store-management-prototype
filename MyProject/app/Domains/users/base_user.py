from Domains.FieldValidatorMixin import FieldValidatorMixin
import jdatetime
from datetime import datetime


class User(FieldValidatorMixin):
    STATUS_PENDING = 'pending'
    STATUS_ACTIVE = 'active'
    STATUS_SUSPENDED = 'suspended'

    def __init__(self):
        self.id = "id"
        self._name = "None"
        self._family = "None"
        self._mobile = "None"
        self._email = "None"
        self._address = "None"
        self._city = "None"
        self._username = "none"
        self._password = "None"
        self._birthday = "None"
        self._gender = "None"
        self._age = "0"
        self.status = self.STATUS_PENDING

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = self._validate_name(value)

    @property
    def family(self):
        return self._family

    @family.setter
    def family(self, value):
        self._family = self._validate_family(value)

    @property
    def mobile(self):
        return self._mobile

    @mobile.setter
    def mobile(self, value):
        self._mobile = self._validate_mobile(value)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = self._validate_email(value)

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = self._validate_address(value)

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, value):
        self._city = self._validate_name(value)

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = self._validate_email(value)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = self._validate_password(value)

    @property
    def birthday(self):
        return self._birthday

    @birthday.setter
    def birthday(self, value):
        self._birthday = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        self._age = self.calculate_age_jalali()

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        self._gender = self._validate_gender(value)

    def __str__(self):
        return f"{self._name} {self._family} ({self._username}) - Status: {self.status}"

    def activate(self):
        self.status = self.STATUS_ACTIVE

    def suspend(self):
        self.status = self.STATUS_SUSPENDED

    def calculate_age_jalali(self):
        if not self.birthday:
            return "تاریخ تولد ثبت نشده است"

        try:
            birth_date = jdatetime.datetime.strptime(self.birthday, "%Y-%m-%d").date()
            today = jdatetime.date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

            if not (0 <= age <= 150):
                return

            return str(age)
        except ValueError:
            return

    def update_info(self, **kwargs):
        for key, value in kwargs.items():
            prop = getattr(self.__class__, key, None)
            if isinstance(prop, property) and prop.fset:
                setattr(self, key, value)
            else:
                raise AttributeError(f"Field '{key}' is not editable or doesn't exist.")

    def get_full_name(self):
        return f"{self._name} {self._family}"

    def to_dict(self):
        return {
            "username": self._username,
            "password": self._password,
            "name": self._name,
            "family": self._family,
            "mobile": self._mobile,
            "email": self._email,
            "address": self._address,
            "city": self._city,
            "birthday": self._birthday,
            "gender": self._gender,
            "status": self.status,
            "age": self.calculate_age_jalali()
        }


class Customer(User):
    def __init__(self):
        super().__init__()
        self._register_date = datetime.now().strftime("%Y-%m-%d")
        self._position = "customer"
        self._digital_wallet = 0.0
        self._loyalty_points = 0
        self._favorite_sellers = []
        self._order_history = []
        self._addresses = []

    @property
    def register_date(self):
        return self._register_date

    @register_date.setter
    def register_date(self, value):
        self._register_date = self._validate_register_date(value)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = self._validate_position(value)

    @property
    def digital_wallet(self):
        return self._digital_wallet

    @digital_wallet.setter
    def digital_wallet(self, value):
        self._digital_wallet = self._validate_digital_wallet(value)

    @property
    def loyalty_points(self):
        return self._loyalty_points

    @loyalty_points.setter
    def loyalty_points(self, value):
        self._loyalty_points = self._validate_loyalty_points(value)

    @property
    def favorite_sellers(self):
        return self._favorite_sellers

    @property
    def order_history(self):
        return self._order_history

    @property
    def addresses(self):
        return self._addresses

    def add_address(self, address):
        if address not in self._addresses:
            self._addresses.append(address)

    def set_default_address(self, address):
        if address in self._addresses:
            self._addresses.remove(address)
            self._addresses.insert(0, address)

    def add_favorite_seller(self, seller):
        if seller not in self._favorite_sellers:
            self._favorite_sellers.append(seller)

    def remove_favorite_seller(self, seller):
        if seller in self._favorite_sellers:
            self._favorite_sellers.remove(seller)

    def add_points(self, points):
        self.loyalty_points += points

    def redeem_points(self, points):
        if points > self.loyalty_points:
            raise ValueError("امتیاز کافی نیست")
        self.loyalty_points -= points

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "loyalty_points": self.loyalty_points,
            "register_date": self.register_date,
            "position": self.position,
            "digital_wallet": self.digital_wallet,
            "favorite_sellers": self.favorite_sellers,
            "order_history": self.order_history,
            # "cart": self.cart,
            "addresses": self.addresses

        })
        return base


class Employee(User):
    def __init__(self):
        super().__init__()
        self._employee_id = "None"
        self._department = "None"
        self._position = "employee"
        self._salary = 0.0
        self._branch = "None"
        self._hire_date = datetime.now().strftime("%Y-%m-%d")
        self._attendance_records = []

    @property
    def employee_id(self):
        return self._employee_id

    @employee_id.setter
    def employee_id(self, value):
        self._employee_id = self._validate_employee_id(value)

    @property
    def department(self):
        return self._department

    @department.setter
    def department(self, value):
        self._department = self._validate_department(value)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = self._validate_position(value)

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        self._salary = self._validate_salary(value)

    @property
    def branch(self):
        return self._branch

    @branch.setter
    def branch(self, value):
        self._branch = self._validate_branch(value)

    @property
    def hire_date(self):
        return self._hire_date

    @hire_date.setter
    def hire_date(self, value):
        self._hire_date = self._validate_hire_date(value)

    @property
    def attendance_records(self):
        return self._attendance_records

    def update_salary(self, new_salary):
        if new_salary >= 0:
            self._salary = new_salary
        else:
            raise ValueError("حقوق نمی‌تواند منفی باشد")

    def transfer_branch(self, new_branch):
        self._branch = new_branch

    def get_attendance_report(self, start_date=None, end_date=None):
        if not start_date:
            start_date = datetime.now().strftime("%Y-%m-01")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        filtered_records = [
            record for record in self._attendance_records
            if start_date <= record["date"] <= end_date
        ]

        return {
            "total_days": len(filtered_records),
            "present_days": len([r for r in filtered_records if r["status"] == "present"]),
            "absent_days": len([r for r in filtered_records if r["status"] == "absent"]),
            "late_days": len([r for r in filtered_records if r["status"] == "late"])
        }

    def update_position(self, new_position):
        self._position = new_position

    def record_attendance(self, status, date=None):
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        record = {
            "date": date,
            "status": status,
            "time": datetime.now().strftime("%H:%M:%S")
        }
        self._attendance_records.append(record)

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "department": self.department,
            "position": self.position,
            "salary": self.salary,
            "branch": self.branch,
            "hire_date": self.hire_date,
            "attendance_records": self.attendance_records
        })
        return base


class Seller(User):
    def __init__(self):
        super().__init__()
        self._shop_name = "Shop"
        self._register_date = datetime.now().strftime("%Y-%m-%d")
        self._position = "seller"
        self._business_license = 1234567890
        self._tax_number = 1234567890
        self._bank_account = 1111111111111111
        self._rating = 0.0
        self._total_sales = 0.0

    @property
    def shop_name(self):
        return self._shop_name

    @shop_name.setter
    def shop_name(self, value):
        self._shop_name = self._validate_shop_name(value)

    @property
    def register_date(self):
        return self._register_date

    @register_date.setter
    def register_date(self, value):
        self._register_date = self._validate_register_date(value)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = self._validate_position(value)

    @property
    def business_license(self):
        return self._business_license

    @business_license.setter
    def business_license(self, value):
        self._business_license = self._validate_business_license(value)

    @property
    def tax_number(self):
        return self._tax_number

    @tax_number.setter
    def tax_number(self, value):
        self._tax_number = self._validate_tax_number(value)

    @property
    def bank_account(self):
        return self._bank_account

    @bank_account.setter
    def bank_account(self, value):
        self._bank_account = self._validate_bank_account(value)

    @property
    def rating(self):
        return self._rating

    @property
    def total_sales(self):
        return self._total_sales



    def get_sales_report(self, start_date=None, end_date=None):
        # این متد باید با سیستم گزارش‌گیری پیاده‌سازی شود
        return {
            "total_sales": self._total_sales,
            "average_rating": self._rating
        }

    def update_rating(self, new_rating):
        if 0 <= new_rating <= 5:
            self._rating = new_rating
        else:
            raise ValueError("امتیاز باید بین 0 تا 5 باشد")

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "shop_name": self.shop_name,
            "register_date": self.register_date,
            "position": self.position,
            "business_license": self.business_license,
            "tax_number": self.tax_number,
            "bank_account": self.bank_account,
            "rating": self.rating,
            "total_sales": self.total_sales,
        })
        return base
