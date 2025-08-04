import re
from typing import List, Dict, Optional, Tuple
from collections import namedtuple
from Application.services.hashing_service import HashingService

hashing_service = HashingService()


def invalid_input(prompt: str, regex: str, errormessage: str, confirm=False,
                  confirm_prompt="لطفا رمز عبور را دوباره وارد نمایید: ",
                  confirm_error="رمز عبور ها مطابقت ندارند. لطفا دوباره تلاش کنید.") -> Optional[str]:
    while True:
        try:
            user_input = input(prompt)
            upper_input = user_input.upper()
            if re.match(regex, user_input):
                if confirm:
                    confirm_password = input(confirm_prompt)
                    if user_input == confirm_password:
                        return user_input.lower()
                    else:
                        raise ValueError(confirm_error)
                else:
                    return user_input
            else:
                raise ValueError(errormessage)
        except ValueError as e:
            print(f"⚠️ خطا: {e}")


def get_common_fields() -> tuple[
     str | None, str | None, str | None, str | None, str | None, str | None, str | None, str | None]:
    name = invalid_input("لطفا نام خود را وارد نمایید", r'^[a-zA-Z\u0600-\u06FF]{2,}$',
                         "Name must contain only letters (2-50 characters).❌")
    family = invalid_input("لطفا نام خانوادگی  خود را وارد نمایید", r'^[a-zA-Z\u0600-\u06FF]{2,}$',
                           "Family must contain only letters (2-50 characters).❌")
    mail = invalid_input("لطفا ایمیل خود را وارد نمایید✉️", r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                         "Email format is incorrect! Example: info@company.com❌")

    password = invalid_input("لطفا رمز عبور خود را وارد نمایید 🔐", r'[A-Za-z]',
                             "Password must contain at least 8 characters, including letters and numbers❌",
                             confirm=True)

    mobile = invalid_input("لطفا موبایل خود را وارد نمایید", r'^09\d{9}$',
                           "Mobile number format is incorrect! Example: "
                           "+989123334444 or 09123334444❌")

    birthday = invalid_input("لطفا تاریخ تولد خود را وارد نمایید مثال yyyy-mm-dd 📆", r'^\d{4}-\d{2}-\d{2}$',
                             "Birth date format is incorrect! Example: yyyy-mm-dd❌")

    address = invalid_input("📍لطفا آدرس دقیق خود را وارد نمایید", r'^[a-zA-Z0-9_.]{5,255}$',
                            "آدرس حداقل 10 کارکتر باشد❌!!!")
    city = invalid_input("📍شهر خود را وارد نمایید", r'^[a-zA-Z0-9_.]{2,50}$',
                         "آدرس حداقل 2 کارکتر باشد❌!!!")

    return name, family, mail, password, mobile, birthday, address, city


def get_product_fields() -> tuple[str | None, str | None, float]:
    name = invalid_input("لطفا نام کالا را وارد نمایید", r'^[a-zA-Z\u0600-\u06FF]{2,}$',
                         "Name must contain only letters (2-50 characters).❌")

    description = invalid_input("لطفا توضیحات کالا را وارد نمایید✉️",
                                r'^[a-zA-Z\u0600-\u06FF]{10,255}$',
                                "description must contain only letters (10-50 characters).❌")

    price = float(invalid_input("لطفا قیمت کالا را وارد نمایید 🔐", r'^\d{4,}$',
                                "قیمت وارد شده قابل قبول نمیباشد❌", ))

    info = (name, description, price)

    return info


def choose_from_valid_data(field_name: str, valid_data: dict) -> Optional[str]:
    values = valid_data.get(field_name)
    if not values:
        print(f"[!] '{field_name}' موجود نیست.")
        return None

    print(f"\n📋 انتخاب {field_name}:")
    for idx, item in enumerate(values, start=1):
        print(f"{idx}. {item}")

    try:
        choice = int(input("🔢 شماره گزینه را وارد کنید: "))
        if 1 <= choice <= len(values):
            return values[choice - 1]
        else:
            print("⛔ شماره وارد شده معتبر نیست.")
            return None
    except ValueError:
        print("⛔ لطفاً یک عدد وارد کنید.")
        return None


StockInfo = namedtuple("StockInfo", ["product_id", "warehouse_id", "seller_id", "markup", "discount", "quantity"])


def get_stock() -> StockInfo:
    product_id = int(invalid_input("آیدی کالا مورد نظر رو وارد نمایید", r'^\d{4,}$', "⛔ آیدی وارد شده معتبر نیست "))
    warehouse_id = int(invalid_input("آیدی انبار مورد نظر رو وارد نمایید", r'^\d{4,}$', "⛔ آیدی وارد شده معتبر نیست "))
    seller_id = int(invalid_input("آیدی فروشنده مورد نظر رو وارد نمایید", r'^\d{4,}$', "⛔ آیدی وارد شده معتبر نیست "))
    markup = float(invalid_input("مارک آپ وارد نمایید", r'^\d{1,3}$', "⛔ مقدار وارد شده معتبر نیست "))
    discount = float(invalid_input("تخفیف را وارد نمایید", r'^\d{1,3}$', "⛔ مقدار وارد شده معتبر نیست "))
    quantity = int(invalid_input("تعداد مورد نظر رو وارد نمایید", r'^\d{1,2}$', "⛔ تعداد وارد شده معتبر نیست "))

    return StockInfo(product_id, warehouse_id, seller_id, markup, discount, quantity)
