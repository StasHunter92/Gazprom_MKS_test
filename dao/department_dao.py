from typing import Type

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from dao.models.department import Department


# ----------------------------------------------------------------------------------------------------------------------
class DepartmentDAO:
    """Data access object for Department model"""

    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Type[Department]]:
        """
        Get list with all departments in database
        Returns:
            List of department objects
        """
        return self.session.query(Department).all()

    def create(self, data: dict) -> None:
        """
        Add a new department
        Args:
            data: Dictionary with data
        Returns:
            None
        """
        new_obj: Department = Department(**data)
        self.session.add(new_obj)

        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise RuntimeError

    def update(self, old_data: dict, new_data: dict) -> None:
        """
        Update department data
        Args:
            old_data: Dictionary with old data
            new_data: Dictionary with new data
        Returns:
            None
        """
        self.session.query(Department).filter(Department.name == old_data.get('name')).update(new_data)

        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise RuntimeError

    def delete(self, uid: int) -> None:
        """
        Delete department
        Args:
            uid: Id of the department
        Returns:
            None
        """
        self.session.query(Department).filter(Department.id == uid).delete()
        self.session.commit()
