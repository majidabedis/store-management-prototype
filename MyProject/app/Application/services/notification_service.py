from typing import Dict, List, Optional

from Database.mongodb.mongo_db import Notification
from Database.repositories.notification_repository import NotificationRepository


class NotificationService:
    def __init__(self):
        self.notification_repository = NotificationRepository()

    # ***************************mongo.db************************

    def create_notification_mongo(self, data) -> bool:
        return self.notification_repository.create_notif(data) if data else False

    def view_notification_mongo(self, user_id: int = None) -> None:
        return self.notification_repository.view_notif(user_id)

    def delete_notification_mongo(self, notif_id) -> bool:
        self.notification_repository.delete_notif(notif_id)
        return True

    # *******************MY.SQL**************************************

    def get_all_notifications(self) -> List[Dict]:
        return self.notification_repository.get_all()

    def get_notification_by_id(self, notification_id: int) -> Optional[Dict]:
        return self.notification_repository.get_by_id(notification_id)

    def create_notification(self, data: Dict) -> Optional[int]:
        return self.notification_repository.add(data)

    def update_notification(self, notification_id: int, updates: Dict) -> bool:
        return self.notification_repository.update(notification_id, updates)

    def delete_notification(self, notification_id: int) -> bool:
        return self.notification_repository.delete(notification_id)

    def get_user_notifications(self, user_id: int) -> List[Dict]:
        return self.notification_repository.get_by_user_id(user_id)

    def mark_as_read(self, notification_id: int) -> bool:
        return self.notification_repository.update(notification_id, {"is_read": True})
