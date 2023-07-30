from typing import Type

from dao.employee_dao import EmployeeDAO
from dao.models.employee import Employee


# ----------------------------------------------------------------------------------------------------------------------
class EmployeeService:
    """Service for the EmployeeDAO"""

    def __init__(self, dao: EmployeeDAO):
        self.dao = dao

    def get_all(self) -> list[Type[Employee]]:
        """
        Get list with all employees in database
        Returns:
            List of employee objects
        """
        return self.dao.get_all()

    def create(self, data: dict) -> None:
        """
        Add a new employee
        Args:
            data: Dictionary with data
        Returns:
            None
        """
        self.dao.create(data)

    def update(self, old_data: dict, new_data: dict) -> None:
        """
        Update employee data
        Args:
            old_data: Dictionary with old data
            new_data: Dictionary with new data
        Returns:
            None
        """
        self.dao.update(old_data, new_data)

    def delete(self, uid: int) -> None:
        """
        Delete employee
        Args:
            uid: ID of the employee
        Returns:
            None
        """
        self.dao.delete(uid)
