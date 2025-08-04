from datetime import datetime
from Domains.FieldValidatorMixin import FieldValidatorMixin
import jdatetime


class Product(FieldValidatorMixin):
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    STATUS_DELETED = 'deleted'

    def __init__(self):
        self._name = "None"
        self._category = "None"
        self._brand = "None"
        self._model = "None"
        self._description = "None"
        self._price = 0.0
        self._markup = 0.0
        self._sale_price = 0.0
        self._warranty_months = 0
        self._created_at = datetime.today()
        self._updated_at = datetime.today()
        self._status = self.STATUS_ACTIVE
        self._images = []
        self._color = "None"

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):

        self._color = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = self._validate_name(value)

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = self._validate_category(value)

    @property
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, value):
        self._brand = self._validate_brand(value)

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = self._validate_model(value)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = self._validate_description(value)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = self._validate_price(value)
        self._sale_price = self._calculate_sale_price(self._price)

    @property
    def markup(self):
        return self._markup

    @markup.setter
    def markup(self, value):
        self._markup = self._validate_markup(value)
        self._sale_price = self._calculate_sale_price(self._price)

    @property
    def sale_price(self):
        return self._sale_price

    @property
    def warranty_months(self):
        return self._warranty_months

    @warranty_months.setter
    def warranty_months(self, value):
        self._warranty_months = self._validate_warranty_months(value)

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        self._created_at = self._validate_hire_date(value)

    @property
    def updated_at(self):
        return self._updated_at

    @updated_at.setter
    def updated_at(self, value):
        self._updated_at = self._validate_hire_date(value)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = self._validate_name(value)

    @property
    def images(self):
        return self._images

    def add_image(self, image_url):
        if image_url not in self._images:
            self._images.append(image_url)
            self._updated_at = jdatetime.date.today().strftime("%Y-%m-%d")

    def remove_image(self, image_url):
        if image_url in self._images:
            self._images.remove(image_url)
            self._updated_at = jdatetime.date.today().strftime("%Y-%m-%d")

    # def update_stock(self, quantity):
    #     if self._stock + quantity < 0:
    #         raise ValueError("موجودی نمی‌تواند منفی باشد")
    #     self._stock += quantity
    #     self._updated_at = jdatetime.date.today().strftime("%Y-%m-%d")
    def _calculate_sale_price(self, value):
        return value + (value * self._markup / 100)

    def deactivate(self):
        self._status = self.STATUS_INACTIVE
        self._updated_at = jdatetime.date.today().strftime("%Y-%m-%d")

    def activate(self):
        self._status = self.STATUS_ACTIVE
        self._updated_at = jdatetime.date.today().strftime("%Y-%m-%d")

    def delete(self):
        self._status = self.STATUS_DELETED
        self._updated_at = jdatetime.date.today().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category,
            "brand": self.brand,
            "model": self.model,
            "description": self.description,
            "color": self.color,
            "price": self.price,
            "markup": self.markup,
            "sale_price": self.sale_price,
            "warranty": self.warranty_months,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status": self.status,
            "images": self.images
        }


class Laptop(Product):
    def __init__(self):
        super().__init__()
        self._screen_size = "None"
        self._processor = "None"
        self._ram = 0
        self._storage = 0
        self._graphics_card = "None"
        self._battery_life = 0
        self._weight = 0.0
        self._os = "None"
        self._product_spect = {}
        self._parent_category = "digital_electric"

    @property
    def screen_size(self):
        return self._screen_size

    @screen_size.setter
    def screen_size(self, value):
        self._screen_size = self._validate_screen_size(value)

    @property
    def processor(self):
        return self._processor

    @processor.setter
    def processor(self, value):
        self._processor = self._validate_processor(value)

    @property
    def ram(self):
        return self._ram

    @ram.setter
    def ram(self, value):
        self._ram = self._validate_ram(value)

    @property
    def storage(self):
        return self._storage

    @storage.setter
    def storage(self, value):
        self._storage = self._validate_storage(value)

    @property
    def graphics_card(self):
        return self._graphics_card

    @graphics_card.setter
    def graphics_card(self, value):
        self._graphics_card = self._validate_graphics_card(value)

    @property
    def battery_life(self):
        return self._battery_life

    @battery_life.setter
    def battery_life(self, value):
        self._battery_life = self._validate_battery_life(value)

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = self._validate_weight(value)

    @property
    def os(self):
        return self._os

    @os.setter
    def os(self, value):
        self._os = self._validate_os(value)

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update(
            {"product_spect": [{
                "screen_size": self.screen_size,
                "processor": self.processor,
                "ram": self.ram,
                "storage": self.storage,
                "graphics_card": self.graphics_card,
                "battery_life": self.battery_life,
                "weight": self.weight,
                "os": self.os
            }],
                "parent_category": self._parent_category
            })

        return base_dict


class Camera(Product):
    def __init__(self):
        super().__init__()
        self._sensor_type = "None"
        self._sensor_size = "None"
        self._resolution = "None"
        self._lens_type = "None"
        self._lens_mount = "None"
        self._iso_range = "None"
        self._shutter_speed = "0"
        self._video_resolution = "None"
        self._product_spect = {}
        self._parent_category = "digital_electric"

    @property
    def sensor_type(self):
        return self._sensor_type

    @sensor_type.setter
    def sensor_type(self, value):
        self._sensor_type = self._validate_sensor_type(value)

    @property
    def sensor_size(self):
        return self._sensor_size

    @sensor_size.setter
    def sensor_size(self, value):
        self._sensor_size = self._validate_sensor_size(value)

    @property
    def resolution(self):
        return self._resolution

    @resolution.setter
    def resolution(self, value):
        self._resolution = self._validate_resolution(value)

    @property
    def lens_type(self):
        return self._lens_type

    @lens_type.setter
    def lens_type(self, value):
        self._lens_type = self._validate_lens_type(value)

    @property
    def lens_mount(self):
        return self._lens_mount

    @lens_mount.setter
    def lens_mount(self, value):
        self._lens_mount = self._validate_lens_mount(value)

    @property
    def iso_range(self):
        return self._iso_range

    @iso_range.setter
    def iso_range(self, value):
        self._iso_range = self._validate_iso_range(value)

    @property
    def shutter_speed(self):
        return self._shutter_speed

    @shutter_speed.setter
    def shutter_speed(self, value):
        self._shutter_speed = self._validate_shutter_speed(value)

    @property
    def video_resolution(self):
        return self._video_resolution

    @video_resolution.setter
    def video_resolution(self, value):
        self._video_resolution = self._validate_video_resolution(value)

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update(
            {"product_spect": [{
                "sensor_type": self.sensor_type,
                "sensor_size": self.sensor_size,
                "resolution": self.resolution,
                "lens_type": self.lens_type,
                "lens_mount": self.lens_mount,
                "iso_range": self.iso_range,
                "shutter_speed": self.shutter_speed,
                "video_resolution": self.video_resolution
            }],
                "parent_category": self._parent_category
            })

        return base_dict


class Mobile(Product):
    def __init__(self):
        super().__init__()
        self._screen_size = "None"
        self._ram = 0
        self._storage = 0
        self._battery_capacity = 0
        self._os = "None"
        self._camera_resolution = "None"
        self._processor = "None"
        self._product_spect = {}
        self._parent_category = "digital_electric"

    @property
    def screen_size(self):
        return self._screen_size

    @screen_size.setter
    def screen_size(self, value):
        self._screen_size = self._validate_resolution(value)

    @property
    def ram(self):
        return self._ram

    @ram.setter
    def ram(self, value):
        self._ram = self._validate_ram(value)

    @property
    def storage(self):
        return self._storage

    @storage.setter
    def storage(self, value):
        self._storage = self._validate_storage(value)

    @property
    def battery_capacity(self):
        return self._battery_capacity

    @battery_capacity.setter
    def battery_capacity(self, value):
        self._battery_capacity = self._validate_battery_capacity(value)

    @property
    def os(self):
        return self._os

    @os.setter
    def os(self, value):
        self._os = self._validate_os(value)

    @property
    def camera_resolution(self):
        return self._camera_resolution

    @camera_resolution.setter
    def camera_resolution(self, value):
        self._camera_resolution = self._validate_camera_resolution(value)

    @property
    def processor(self):
        return self._processor

    @processor.setter
    def processor(self, value):
        self._processor = self._validate_processor(value)

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update(
            {"product_spect": [{
                "screen_size": self.screen_size,
                "ram": self.ram,
                "storage": self.storage,
                "battery_capacity": self.battery_capacity,
                "os": self.os,
                "camera_resolution": self.camera_resolution,
                "processor": self.processor
            }],
                "parent_category": self._parent_category
            })

        return base_dict
