from typing import Optional
from Application.interfaces.panel_interface import (IPanel, IAdminWarehousePanel, ISuperAdminPanel,
                                                    ICustomerPanel, ISellerPanel, IEmployeePanel)
from Application.panels.admin_warehouse import AdminWarehousePanel
from Application.panels.admin_users import AdminUsersPanel
from Application.panels.admin_order import AdminOrderPanel
from Application.panels.super_admin_panel import SuperAdminPanel
from Application.panels.customer_panel import CustomerPanel
from Application.panels.seller_panel import SellerPanel
from Application.panels.employee_panel import EmployeePanel


class PanelFactory:
    @staticmethod
    def create_panel(user_type: str, user_id: int) -> Optional[IPanel]:
        """
        Create a panel based on user type.
        :param user_type:   (admin, customer, seller, employee)
        :param user_id:
        :return: user panel
        """
        panel_map = {
            "super_admin": SuperAdminPanel,
            "admin_warehouse": AdminWarehousePanel,
            "admin_users": AdminUsersPanel,
            "admin_order": AdminOrderPanel,
            "customer": CustomerPanel,
            "seller": SellerPanel,
            "employee": EmployeePanel
        }
        panel_class = panel_map.get(user_type.lower())
        if panel_class:
            return panel_class(user_id)
        else:
            print("Error")
        return None
