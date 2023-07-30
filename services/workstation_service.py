from typing import Type

from dao.models.workstation import Workstation
from dao.workstation_dao import WorkstationDAO


# ----------------------------------------------------------------------------------------------------------------------
class WorkstationService:
    """Service for the WorkstationDAO"""

    def __init__(self, dao: WorkstationDAO):
        self.dao = dao

    def get_all(self) -> list[Type[Workstation]]:
        """
        Get list with all workstations in database
        Returns:
            List of workstation objects
        """
        return self.dao.get_all()

    def create(self, data: dict) -> None:
        """
        Add a new workstation
        Args:
            data: Dictionary with data
        Returns:
            None
        """
        self.dao.create(data)

    def update(self, old_data: dict, new_data: dict) -> None:
        """
        Update workstation data
        Args:
            old_data: Dictionary with old data
            new_data: Dictionary with new data
        Returns:
            None
        """
        self.dao.update(old_data, new_data)

    def delete(self, uid: int) -> None:
        """
        Delete workstation
        Args:
            uid: ID of the workstation
        Returns:
            None
        """
        self.dao.delete(uid)
