from typing import Type

from dao.cable_line_dao import CableLineDAO
from dao.models.cable_line import CableLine


# ----------------------------------------------------------------------------------------------------------------------
class CableLineService:
    """Service for the CableLineDAO"""

    def __init__(self, dao: CableLineDAO):
        self.dao = dao

    def get_all(self) -> list[Type[CableLine]]:
        """
        Get list with all cable lines in database
        Returns:
            List of cable line objects
        """
        return self.dao.get_all()

    def create(self, data: dict) -> None:
        """
        Add a new cable line
        Args:
            data: Dictionary with data
        Returns:
            None
        """
        return self.dao.create(data)

    def update(self, old_data: dict, new_data: dict) -> None:
        """
        Update cable line data
        Args:
            old_data: Dictionary with old data
            new_data: Dictionary with new data
        Returns:
            None
        """
        self.dao.update(old_data, new_data)

    def delete(self, uid: int) -> None:
        """
        Delete cable line
        Args:
            uid: ID of the cable line
        Returns:
            None
        """
        self.dao.delete(uid)
