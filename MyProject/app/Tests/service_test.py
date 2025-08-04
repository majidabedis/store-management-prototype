from Application.services.user_service import UserService
from Database.repositories.user_repository import UserRepository

repository = UserRepository()
service = UserService()
# service.update_user("customer", {"mobile": "09121234567"}, "position = 'customer'")
data = service.get_user_by_filter("customer", "position = 'customer'")[0]
print(data)
