from Application.services.notification_service import NotificationService

notification_service = NotificationService()


def send_notification(user_id: int, title: str, message: str) -> None:
    if user_id:
        user_id = int(user_id)
        data = {
            "user_id": user_id,
            "title": title,
            "message": message,
        }
        if notification_service.create_notification(data):
            print("اعلان با موفقیت ارسال شد")
        else:
            print("خطا در ارسال اعلان.")
    else:
        if notification_service.create_notification(title, message):
            print("اعلان با موفقیت به همه کاربران ارسال شد.")
        else:
            print("خطا در ارسال اعلان.")
