from typing import Type

from dao.models.server_room import ServerRoom
from dao.server_room_dao import ServerRoomDAO


# ----------------------------------------------------------------------------------------------------------------------
class ServerRoomService:
    """Service for the ServerRoomDAO"""

    def __init__(self, dao: ServerRoomDAO):
        self.dao = dao

    def get_all(self) -> list[Type[ServerRoom]]:
        """
        Get list with all server rooms in database
        Returns:
            List of server room objects
        """
        return self.dao.get_all()

    def create(self, data: dict) -> None:
        """
        Add a new server room
        Args:
            data: Dictionary with data
        Returns:
            None
        """
        self.dao.create(data)

    def update(self, old_data: dict, new_data: dict) -> None:
        """
        Update server room data
        Args:
            old_data: Dictionary with old data
            new_data: Dictionary with new data
        Returns:
            None
        """
        self.dao.update(old_data, new_data)

    def delete(self, uid: int) -> None:
        """
        Delete server room
        Args:
            uid: ID of the server room
        Returns:
            None
        """
        self.dao.delete(uid)
