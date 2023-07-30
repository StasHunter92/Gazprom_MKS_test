from typing import Type

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from dao.models.server_room import ServerRoom


# ----------------------------------------------------------------------------------------------------------------------
class ServerRoomDAO:
    """Data access object for ServerRoom model"""

    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Type[ServerRoom]]:
        """
        Get list with all server rooms in database
        Returns:
            List of server room objects
        """
        return self.session.query(ServerRoom).all()

    def create(self, data: dict) -> None:
        """
        Add a new server room
        Args:
            data: Dictionary with data
        Returns:
            None
        """
        new_obj: ServerRoom = ServerRoom(**data)
        self.session.add(new_obj)

        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise RuntimeError

    def update(self, old_data: dict, new_data: dict) -> None:
        """
        Update server room data
        Args:
            old_data: Dictionary with old data
            new_data: Dictionary with new data
        Returns:
            None
        """
        self.session.query(ServerRoom).filter(
            ServerRoom.number == old_data.get('number')
        ).update(new_data)

        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise RuntimeError

    def delete(self, uid: int) -> None:
        """
        Delete server room
        Args:
            uid: ID of the server room
        Returns:
            None
        """
        self.session.query(ServerRoom).filter(
            ServerRoom.id == uid
        ).delete()
        self.session.commit()
