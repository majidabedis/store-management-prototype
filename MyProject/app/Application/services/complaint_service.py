from typing import Dict, List, Optional
from Database.repositories.complaint_repository import ComplaintRepository

class ComplaintService:
    def __init__(self):
        self.complaint_repository = ComplaintRepository()

    def get_all_complaints(self) -> List[Dict]:
        return self.complaint_repository.get_all()

    def get_complaint_by_id(self, complaint_id: int) -> Optional[Dict]:

        return self.complaint_repository.get_by_id(complaint_id)

    def create_complaint(self, data: Dict) -> Optional[int]:
        return self.complaint_repository.add(data)

    def update_complaint(self, complaint_id: int, updates: Dict) -> bool:
        return self.complaint_repository.update(complaint_id, updates)

    def delete_complaint(self, complaint_id: int) -> bool:
        return self.complaint_repository.delete(complaint_id)

    def get_user_complaints(self, user_id: int) -> List[Dict]:
        return self.complaint_repository.get_by_user_id(user_id)

    def get_pending_complaints(self) -> List[Dict]:
        return self.complaint_repository.get_by_status("pending")

    def get_processing_complaints(self) -> List[Dict]:
        return self.complaint_repository.get_by_status("processing")

    def get_resolved_complaints(self) -> List[Dict]:
        return self.complaint_repository.get_by_status("resolved")

    def update_complaint_status(self, complaint_id: int, status: str) -> bool:
        return self.complaint_repository.update(complaint_id, {"status": status})

    def add_response(self, complaint_id: int, response: str, employee_id: int) -> bool:
        return self.complaint_repository.update(complaint_id, {
            "response": response,
            "employee_id": employee_id,
            "status": "resolved"
        }) 