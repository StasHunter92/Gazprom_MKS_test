from typing import Type

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from dao.models.employee import Employee


# ----------------------------------------------------------------------------------------------------------------------
class EmployeeDAO:
    """Data access object for Employee model"""

    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Type[Employee]]:
        """
        Get list with all employees in database
        Returns:
            List of employee objects
        """
        return self.session.query(Employee).all()

    def create(self, data: dict) -> None:
        """
        Add a new employee
        Args:
            data: Dictionary with data
        Returns:
            None
        """
        new_obj: Employee = Employee(**data)
        self.session.add(new_obj)

        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise RuntimeError

    def update(self, old_data: dict, new_data: dict) -> None:
        """
        Update employee data
        Args:
            old_data: Dictionary with old data
            new_data: Dictionary with new data
        Returns:
            None
        """
        self.session.query(Employee).filter(
            Employee.first_name == old_data.get('first_name'),
            Employee.last_name == old_data.get('last_name'),
            Employee.patronymic == old_data.get('patronymic')
        ).update(new_data)

        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise RuntimeError

    def delete(self, uid: int) -> None:
        """
        Delete employee
        Args:
            uid: ID of the employee
        Returns:
            None
        """
        self.session.query(Employee).filter(Employee.id == uid).delete()
        self.session.commit()
