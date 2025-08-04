from typing import Dict, List, Optional
from Database.repositories.interface import IRepository
from Database.db.connection_manager import DatabaseManager
from Database.mongodb.mongo_db import Notification


class NotificationRepository(IRepository):
    def __init__(self):
        self.table_name = "notifiction"
        self.db = DatabaseManager()
        self.mongodb = Notification()

    ##mongo db
    def create_notif(self, data: dict) -> bool:
        return self.mongodb.create_notification(data) if data else False

    def view_notif(self, user_id: int = None) -> None:
        return self.mongodb.view_notif(user_id)

    def delete_notif(self, notif_id) -> None:
        self.mongodb.delete_notif(notif_id)

    # *******************MY.SQL**************************************

    def get_all(self) -> List[Dict]:
        return self.db.read_data(self.table_name)

    def get_by_id(self, notification_id: int) -> Optional[Dict]:
        result = self.db.read_data(self.table_name, condition=f"id = {notification_id}")
        return result[0] if result else None

    def add(self, data: Dict) -> Optional[int]:
        columns = list(data.keys())
        values = list(data.values())
        insert = self.db.insert_data(self.table_name, columns, values)
        return insert if insert else None
        # return self.db.get_last_insert_id()

    def update(self, notification_id: int, updates: Dict) -> bool:
        condition = f"id = {notification_id}"
        self.db.update_data(self.table_name, updates, condition)
        return True

    def delete(self, notification_id: int) -> bool:
        condition = f"noti_id = {notification_id}"
        self.db.delete_data(self.table_name, condition)
        return True

    def get_by_user_id(self, user_id: int) -> List[Dict]:
        return self.db.read_data(self.table_name, condition=f"user_id = {user_id}")

    def get_unread_notifications(self, user_id: int) -> List[Dict]:
        return self.db.read_data(
            self.table_name,
            condition=f"user_id = {user_id} AND is_read = 0"
        )
