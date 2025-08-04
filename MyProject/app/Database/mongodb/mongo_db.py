from datetime import datetime

import pymongo
from bson import ObjectId


class Notification():
    def __init__(self):
        self.conn = pymongo.MongoClient()
        self.db = self.conn["mini_twitter"]
        self.notification = self.db["notification"]

    def create_notification(self, data: dict) -> bool:
        send = self.notification.insert_one(data)
        if send:
            print("پیام ایجاد شد")
            return send.inserted_id

        else:
            print("پیام ایجاد نشد")
            return False

    def view_notif(self, user_id: int = None) -> None:
        print("\n📋 لیست پیام ها:\n")
        query = {}
        if user_id is not None:
            query["user_id"] = user_id
        results = self.notification.find(query).sort("created_at", -1)
        found = False
        for t in results:
            found = True
            print(f"ID: {str(t['_id'])}")
            print(f"[ {t['title']}  msg: {t['message']} ]\n")
        if not found:
            print("📭 پیامی یافت نشد.")

    def delete_notif(self, notif_id) -> None:
        try:
            result = self.notification.delete_one({"_id": ObjectId(notif_id)})
            if result.deleted_count:
                print("✅ پیام با موفقیت حذف شد!\n")
            else:
                print("❌ پیام با این شناسه پیدا نشد.\n")
        except Exception as e:
            print(f"خطا: {e}\n")
