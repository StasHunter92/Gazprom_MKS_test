from typing import Type

from dao.department_dao import DepartmentDAO
from dao.models.department import Department


# ----------------------------------------------------------------------------------------------------------------------
class DepartmentService:
    """Service for the DepartmentDAO"""

    def __init__(self, dao: DepartmentDAO):
        self.dao = dao

    def get_all(self) -> list[Type[Department]]:
        """
        Get list with all departments in database
        Returns:
            List of department objects
        """
        return self.dao.get_all()

    def create(self, data: dict) -> None:
        """
        Add a new department
        Args:
            data: Dictionary with data
        Returns:
            None
        """
        self.dao.create(data)

    def update(self, old_data: dict, new_data: dict) -> None:
        """
        Update department data
        Args:
            old_data: Dictionary with old data
            new_data: Dictionary with new data
        Returns:
            None
        """
        self.dao.update(old_data, new_data)

    def delete(self, uid: int) -> None:
        """
        Delete department
        Args:
            uid: ID of the department
        Returns:
            None
        """
        self.dao.delete(uid)
