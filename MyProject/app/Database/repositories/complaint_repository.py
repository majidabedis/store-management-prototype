from typing import Dict, List, Optional
from Database.repositories.interface import IRepository
from Database.db.connection_manager import DatabaseManager

class ComplaintRepository(IRepository):
    def __init__(self):
        self.db = DatabaseManager()

    def get_all(self) -> List[Dict]:
        return self.db.read_data("complaints")

    def get_by_id(self, complaint_id: int) -> Optional[Dict]:
        result = self.db.read_data("complaints", condition=f"id = {complaint_id}")
        return result[0] if result else None

    def add(self, data: Dict) -> Optional[int]:
        columns = list(data.keys())
        values = list(data.values())
        self.db.insert_data("complaints", columns, values)
        return self.db.get_last_insert_id()

    def update(self, complaint_id: int, updates: Dict) -> bool:
        set_clause = ", ".join([f"{k} = %s" for k in updates.keys()])
        values = list(updates.values())
        query = f"UPDATE complaints SET {set_clause} WHERE id = %s"
        values.append(complaint_id)
        try:
            self.db.cursor.execute(query, values)
            self.db.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating complaint: {e}")
            return False

    def delete(self, complaint_id: int) -> bool:
        try:
            self.db.delete_data("complaints", f"id = {complaint_id}")
            return True
        except Exception as e:
            print(f"Error deleting complaint: {e}")
            return False

    def get_by_user_id(self, user_id: int) -> List[Dict]:

        return self.db.read_data("complaints", condition=f"user_id = {user_id}")

    def get_by_status(self, status: str) -> List[Dict]:
        return self.db.read_data("complaints", condition=f"status = '{status}'")

    def get_by_employee_id(self, employee_id: int) -> List[Dict]:
        return self.db.read_data("complaints", condition=f"employee_id = {employee_id}") 