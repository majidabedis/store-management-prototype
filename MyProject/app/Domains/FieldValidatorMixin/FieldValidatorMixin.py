import re

import jdatetime


class FieldValidatorMixin:
    sql_keywords = [
        "SELECT", "INSERT", "UPDATE", "DELETE", "DROP",
        "ALTER", "TRUNCATE", "EXEC", "UNION", "CREATE"
    ]

    def check_sql_injection(self, value):
        upper_input = value.upper()
        if any(keyword in upper_input for keyword in self.sql_keywords):
            raise ValueError("ورودی شامل دستورات غیرمجاز است ⚠️")

    def _validate_name(self, value):
        self.check_sql_injection(value)
        if not re.match(r'^[a-zA-Z\u0600-\u06FF]{2,}$', value):
            raise ValueError("فرمت نام معتبر نیست")
        return value

    def _validate_family(self, value):
        self.check_sql_injection(value)
        if not re.match(r'^[a-zA-Z\u0600-\u06FF]{2,}$', value):
            raise ValueError("فرمت نام خانوادگی معتبر نیست")
        return value

    def _validate_mobile(self, value):
        self.check_sql_injection(value)
        if not re.match(r'^09\d{9}$', value):
            raise ValueError("فرمت موبایل معتبر نیست")
        return value

    def _validate_email(self, value):
        self.check_sql_injection(value)
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value):
            raise ValueError("فرمت ایمیل معتبر نیست")
        return value

    def _validate_address(self, value):
        self.check_sql_injection(value)
        if len(value.strip()) < 5:
            raise ValueError("آدرس خیلی کوتاه است")
        return value

    def _validate_username(self, value):
        self.check_sql_injection(value)
        if not re.match(r'^[a-zA-Z0-9_.]{4,20}$', value):
            raise ValueError("فرمت نام کاربری معتبر نیست")
        return value

    def _validate_password(self, value):
        self.check_sql_injection(value)
        if len(value) < 8:
            raise ValueError("رمز عبور حداقل باید ۸ کاراکتر باشد")
        if not re.search(r'[A-Za-z]', value) or not re.search(r'\d', value):
            raise ValueError("رمز عبور باید شامل حروف و عدد باشد")
        return value

    def _validate_phone(self, value):
        self.check_sql_injection(value)
        if not re.match(r'^\d{8,11}$', value):
            raise ValueError("فرمت تلفن معتبر نیست")
        return value

    def _validate_birthday(self, value):
        self.check_sql_injection(value)
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', value):
            raise ValueError("فرمت تاریخ تولد معتبر نیست")
        return value

    def _validate_gender(self, value):
        self.check_sql_injection(value)
        if value not in ['male', 'female', 'unisex']:
            raise ValueError("جنسیت نامعتبر است")
        return value

    def _validate_age(self, value):
        self.check_sql_injection(value)
        try:
            age = int(value)
            if not (0 <= age <= 150):
                raise ValueError("سن باید بین 0 تا 150 سال باشد")
            return str(age)
        except ValueError:
            raise ValueError("سن باید عدد صحیح باشد")

    def _validate_register_date(self, value):
        self.check_sql_injection(value)
        return value

    def _validate_digital_wallet(self, value):
        if value < 0:
            raise ValueError("مقدار وارد شده غلط میباشد ")
        return float(value)

    def _validate_loyalty_points(self, value):
        try:
            points = int(value)
            if points < 0:
                raise ValueError("امتیاز نمی‌تواند منفی باشد")
            return points
        except ValueError:
            raise ValueError("امتیاز باید عدد صحیح باشد")

    def _validate_position(self, value):
        self.check_sql_injection(value)
        if len(value) < 3:
            raise ValueError("مقدار وارد شده غلط میباشد ")
        return value

    def _validate_shop_name(self, value):
        self.check_sql_injection(value)
        if len(value) < 2:
            raise ValueError("مقدار وارد شده غلط میباشد ")
        return value

    def _validate_business_license(self, value):
        if not re.match(r'^\d{10}$', value):
            raise ValueError("فرمت مجوز کسب و کار معتبر نیست")
        return value

    def _validate_tax_number(self, value):
        self.check_sql_injection(value)
        if not re.match(r'^\d{10}$', value):
            raise ValueError("فرمت شماره مالیاتی معتبر نیست")
        return value

    def _validate_bank_account(self, value):
        self.check_sql_injection(value)
        if not re.match(r'^\d{16}$', value):
            raise ValueError("فرمت شماره حساب بانکی معتبر نیست")
        return str(value)

    def _validate_employee_id(self, value):
        return value

    def _validate_department(self, value):
        self.check_sql_injection(value)
        valid_departments = ['sales', 'marketing', 'finance', 'hr', 'it', 'operations']
        if value.lower() not in valid_departments:
            raise ValueError("بخش دپارتمان نامعتبر است")
        return value.lower()

    def _validate_branch(self, value):
        self.check_sql_injection(value)
        if len(value.strip()) < 3:
            raise ValueError("نام شعبه خیلی کوتاه است")
        return value

    def _validate_salary(self, value):
        try:
            salary = float(value)
            if salary < 0:
                raise ValueError("حقوق نمی‌تواند منفی باشد")
            return salary
        except ValueError:
            raise ValueError("حقوق باید عدد باشد")

    def _validate_hire_date(self, value):
        self.check_sql_injection(value)
        try:
            jdatetime.date.fromisoformat(value)
            return value
        except ValueError:
            raise ValueError("فرمت تاریخ استخدام معتبر نیست")

    def _validate_brand(self, value):
        self.check_sql_injection(value)
        if len(value.strip()) < 2:
            raise ValueError("نام برند خیلی کوتاه است")
        return value

    def _validate_model(self, value):
        self.check_sql_injection(value)
        if len(value.strip()) < 2:
            raise ValueError("نام مدل خیلی کوتاه است")
        return value

    def _validate_description(self, value):
        self.check_sql_injection(value)
        if len(value.strip()) < 10:
            raise ValueError("توضیحات خیلی کوتاه است")
        return value

    def _validate_price(self, value):
        try:
            price = float(value)
            if price < 0:
                raise ValueError("قیمت نمی‌تواند منفی باشد")
            return price
        except ValueError:
            raise ValueError("قیمت باید عدد باشد")

    def _validate_markup(self, value):
        try:
            price = float(value)
            if price < 0:
                raise ValueError("مارک آپ نمی‌تواند منفی باشد")
            return price
        except ValueError:
            raise ValueError("قیمت باید عدد باشد")

    def _validate_stock(self, value):
        try:
            stock = int(value)
            if stock < 0:
                raise ValueError("موجودی نمی‌تواند منفی باشد")
            return stock
        except ValueError:
            raise ValueError("موجودی باید عدد صحیح باشد")

    def _validate_category(self, value):
        self.check_sql_injection(value)
        valid_categories = ['mobile', 'camera', 'laptop']
        if value.lower() not in valid_categories:
            raise ValueError("دسته‌بندی نامعتبر است")
        return value.lower()

    def _validate_warranty_months(self, value):
        try:
            months = int(value)
            if months < 0:
                raise ValueError("مدت گارانتی نمی‌تواند منفی باشد")
            if months > 36:
                raise ValueError("مدت گارانتی نمی‌تواند بیشتر از 36 ماه باشد")
            return months
        except ValueError:
            raise ValueError("مدت گارانتی باید عدد صحیح باشد")

    # Mobile specific validations
    def _validate_screen_size(self, value):
        self.check_sql_injection(value)
        if not re.match(r'^\d+(\.\d+)?\s*(inch|"|in)$', value):
            raise ValueError("فرمت اندازه صفحه نمایش نامعتبر است")
        return value

    def _validate_ram(self, value):
        try:
            ram = int(value)
            if ram <= 0:
                raise ValueError("حافظه RAM باید بزرگتر از صفر باشد")
            return ram
        except ValueError:
            raise ValueError("حافظه RAM باید عدد صحیح باشد")

    def _validate_storage(self, value):
        try:
            storage = int(value)
            if storage <= 0:
                raise ValueError("حافظه ذخیره‌سازی باید بزرگتر از صفر باشد")
            return storage
        except ValueError:
            raise ValueError("حافظه ذخیره‌سازی باید عدد صحیح باشد")

    def _validate_battery_capacity(self, value):
        try:
            capacity = int(value)
            if capacity <= 0:
                raise ValueError("ظرفیت باتری باید بزرگتر از صفر باشد")
            return capacity
        except ValueError:
            raise ValueError("ظرفیت باتری باید عدد صحیح باشد")

    def _validate_os(self, value):
        self.check_sql_injection(value)
        valid_os = ['android', 'ios', 'windows', 'macos', 'linux']
        if value.lower() not in valid_os:
            raise ValueError("سیستم عامل نامعتبر است")
        return value.lower()

    def _validate_camera_resolution(self, value):
        # self.check_sql_injection(value)
        if not re.match(r'^\d+MP$', value):
            raise ValueError("فرمت رزولوشن دوربین نامعتبر است")
        return value

    def _validate_resolution(self, value):
        # self.check_sql_injection(value)
        if not re.match(r'^\d+PX$', value):
            raise ValueError("فرمت رزولوشن دوربین نامعتبر است")
        return value

    def _validate_processor(self, value):
        self.check_sql_injection(value)
        if len(value.strip()) < 2:
            raise ValueError("نام پردازنده خیلی کوتاه است")
        return value

    # Camera specific validations
    def _validate_sensor_type(self, value):
        self.check_sql_injection(value)
        valid_sensors = ['cmos', 'ccd', 'bsi-cmos']
        if value.lower() not in valid_sensors:
            raise ValueError("نوع سنسور نامعتبر است")
        return value.lower()

    def _validate_sensor_size(self, value):
        # self.check_sql_injection(value)
        if not re.match(r'^\d+(\.\d+)?\s*(mm|MP)$', value):
            raise ValueError("فرمت اندازه سنسور نامعتبر است")
        return value

    def _validate_lens_type(self, value):
        self.check_sql_injection(value)
        valid_lenses = ['prime', 'zoom', 'macro', 'wide-angle', 'telephoto']
        if value.lower() not in valid_lenses:
            raise ValueError("نوع لنز نامعتبر است")
        return value.lower()

    def _validate_lens_mount(self, value):
        self.check_sql_injection(value)
        valid_mounts = ['ef', 'ef-s', 'rf', 'f', 'z', 'e', 'x', 'mft']
        if value.lower() not in valid_mounts:
            raise ValueError("نوع پایه لنز نامعتبر است")
        return value.lower()

    def _validate_iso_range(self, value):
        valid_ranges = ['100', '200', '400', '800', '1600']
        if value not in valid_ranges:
            raise ValueError("نوع ایزو نا معتبر است ")
        return value

    def _validate_shutter_speed(self, value):
        # self.check_sql_injection(value)
        if not re.match(r'^\d+-\d+$', str(value)):
            raise ValueError("فرمت سرعت شاتر نامعتبر است")
        return value

    def _validate_video_resolution(self, value):
        self.check_sql_injection(value)
        valid_resolutions = ['4k', '1080p', '720p', '480p']
        if value.lower() not in valid_resolutions:
            raise ValueError("رزولوشن ویدیو نامعتبر است")
        return value.lower()

    # Laptop specific validations
    def _validate_graphics_card(self, value):
        self.check_sql_injection(value)
        if len(value.strip()) < 2:
            raise ValueError("نام کارت گرافیک خیلی کوتاه است")
        return value

    def _validate_battery_life(self, value):
        try:
            hours = int(value)
            if hours <= 0:
                raise ValueError("زمان کار باتری باید بزرگتر از صفر باشد")
            return hours
        except ValueError:
            raise ValueError("زمان کار باتری باید عدد صحیح باشد")

    def _validate_weight(self, value):
        try:
            weight = float(value)
            if weight <= 0:
                raise ValueError("وزن باید بزرگتر از صفر باشد")
            return weight
        except ValueError:
            raise ValueError("وزن باید عدد باشد")
