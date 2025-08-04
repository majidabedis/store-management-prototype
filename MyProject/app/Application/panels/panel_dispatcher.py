from typing import Optional
from Application.factories.panel_factory import PanelFactory
from Application.interfaces.panel_interface import IPanel


class PanelDispatcher:
    @staticmethod
    def dispatch(user_type: str, user_id: int) -> Optional[IPanel]:
        """
        create and return user panel on user type
        :param user_type: user position (admin, customer, seller, employee ,super_admin)
        :param user_id: user id
        :return: return user panel on user type
        """
        panel = PanelFactory.create_panel(user_type, user_id)
        return panel
