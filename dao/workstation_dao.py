from typing import Type

from sqlalchemy.exc import IntegrityError

from dao.models.workstation import Workstation


# ----------------------------------------------------------------------------------------------------------------------
class WorkstationDAO:
    """Data access object for Department model"""

    def __init__(self, session):
        self.session = session

    def get_all(self) -> list[Type[Workstation]]:
        """
        Get list with all workstations in database
        Returns:
            List of workstation objects
        """
        return self.session.query(Workstation).all()

    def create(self, data: dict) -> None:
        """
        Add a new workstation
        Args:
            data: Dictionary with data
        Returns:
            None
        """
        new_obj: Workstation = Workstation(**data)
        self.session.add(new_obj)

        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise RuntimeError

    def update(self, old_data: dict, new_data: dict) -> None:
        """
        Update workstation data
        Args:
            old_data: Dictionary with old data
            new_data: Dictionary with new data
        Returns:
            None
        """
        self.session.query(Workstation).filter(Workstation.name == old_data.get('name')).update(new_data)

        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise RuntimeError

    def delete(self, uid: int) -> None:
        """
        Delete workstation
        Args:
            uid: Id of the workstation
        Returns:
            None
        """
        self.session.query(Workstation).filter(Workstation.id == uid).delete()
        self.session.commit()
