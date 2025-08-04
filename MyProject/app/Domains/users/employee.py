from Domains.users import BaseUser
from datetime import datetime


class Employee(BaseUser):
    def __init__(self):
        super().__init__()
        self._employee_id = None
        self._department = None
        self._position = "employee"
        self._salary = 0.0
        self._branch = None
        self._hire_date = datetime.now().strftime("%Y-%m-%d")
        self._attendance_records = []

    @property
    def employee_id(self):
        return self._employee_id

    @employee_id.setter
    def employee_id(self, value):
        self._employee_id = self._validate_employee_id(value)

    @property
    def department(self):
        return self._department

    @department.setter
    def department(self, value):
        self._department = self._validate_department(value)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = self._validate_position(value)

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        self._salary = self._validate_salary(value)

    @property
    def branch(self):
        return self._branch

    @branch.setter
    def branch(self, value):
        self._branch = self._validate_branch(value)

    @property
    def hire_date(self):
        return self._hire_date

    @hire_date.setter
    def hire_date(self, value):
        self._hire_date = self._validate_hire_date(value)

    @property
    def attendance_records(self):
        return self._attendance_records

    def update_salary(self, new_salary):
        if new_salary >= 0:
            self._salary = new_salary
        else:
            raise ValueError("حقوق نمی‌تواند منفی باشد")

    def transfer_branch(self, new_branch):
        self._branch = new_branch

    def get_attendance_report(self, start_date=None, end_date=None):
        if not start_date:
            start_date = datetime.now().strftime("%Y-%m-01")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        filtered_records = [
            record for record in self._attendance_records
            if start_date <= record["date"] <= end_date
        ]

        return {
            "total_days": len(filtered_records),
            "present_days": len([r for r in filtered_records if r["status"] == "present"]),
            "absent_days": len([r for r in filtered_records if r["status"] == "absent"]),
            "late_days": len([r for r in filtered_records if r["status"] == "late"])
        }

    def update_position(self, new_position):
        self._position = new_position

    def record_attendance(self, status, date=None):
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        record = {
            "date": date,
            "status": status,
            "time": datetime.now().strftime("%H:%M:%S")
        }
        self._attendance_records.append(record)

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "employee_id": self.employee_id,
            "department": self.department,
            "position": self.position,
            "salary": self.salary,
            "branch": self.branch,
            "hire_date": self.hire_date,
            "attendance_records_count": len(self.attendance_records)
        })
        return base
