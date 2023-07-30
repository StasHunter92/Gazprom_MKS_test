from typing import Type

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from dao.models.cable_line import CableLine
from dao.models.employee import Employee
from dao.models.workstation import Workstation


# ----------------------------------------------------------------------------------------------------------------------
class CableLineDAO:
    """Data access object for CableLine model"""

    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Type[CableLine]]:
        """
        Get list with all cable lines in database
        Returns:
            List of cable line objects
        """
        return self.session.query(CableLine).join(Employee).join(Workstation).all()

    def create(self, data: dict) -> None:
        """
        Add a new cable line
        Args:
            data: Dictionary with data
        Returns:
            None
        """
        new_obj: CableLine = CableLine(**data)
        self.session.add(new_obj)

        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise RuntimeError

    def update(self, old_data: dict, new_data: dict) -> None:
        """
        Update cable line data
        Args:
            old_data: Dictionary with old data
            new_data: Dictionary with new data
        Returns:
            None
        """
        self.session.query(CableLine).filter(
            CableLine.id == old_data.get('id'),
        ).update(new_data)

        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise RuntimeError

    def delete(self, uid: int) -> None:
        """
        Delete cable line
        Args:
            uid: ID of the cable line
        Returns:
            None
        """
        self.session.query(CableLine).filter(CableLine.id == uid).delete()
        self.session.commit()
