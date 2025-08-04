from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class IPanel(ABC):
    @abstractmethod
    def show_menu(self) -> None:
        pass

    @abstractmethod
    def handle_menu_choice(self, choice: str) -> None:
        pass


class ISuperAdminPanel(IPanel):

    @abstractmethod
    def manage_users(self) -> None:
        pass

    @abstractmethod
    def manage_products(self) -> None:
        pass

    @abstractmethod
    def manage_notifications(self) -> None:
        pass

    @abstractmethod
    def manage_warehouse(self) -> None:
        pass

    @abstractmethod
    def _manage_orders(self) -> None:
        pass


class ICustomerPanel(IPanel):
    @abstractmethod
    def view_products(self) -> None:
        pass

    @abstractmethod
    def manage_cart(self) -> None:
        pass

    @abstractmethod
    def view_profile(self) -> None:
        pass

    @abstractmethod
    def edit_profile(self) -> None:
        pass


class ISellerPanel(IPanel):
    @abstractmethod
    def manage_products(self) -> None:
        pass

    @abstractmethod
    def view_orders(self) -> None:
        pass

    @abstractmethod
    def manage_profile(self) -> None:
        pass


class IEmployeePanel(IPanel):
    @abstractmethod
    def manage_orders(self) -> None:
        pass

    @abstractmethod
    def manage_complaints(self) -> None:
        pass

    @abstractmethod
    def view_reports(self) -> None:
        pass


class IAdminWarehousePanel(IPanel):
    @abstractmethod
    def _manage_warehouse(self) -> None:
        pass


class IAdminUsersPanel(IPanel):
    @abstractmethod
    def _manage_users(self) -> None:
        pass


class IAdminProductsPanel(IPanel):
    @abstractmethod
    def _manage_products(self) -> None:
        pass


class IAdminOrdersPanel(IPanel):
    @abstractmethod
    def _manage_orders(self) -> None:
        pass
