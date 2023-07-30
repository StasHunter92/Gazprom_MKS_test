from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from dao.models.base_model import Base
from dao.models.department import Department


# ----------------------------------------------------------------------------------------------------------------------
class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    patronymic = Column(String(50))
    department_id = Column(Integer, ForeignKey('departments.id'), index=True)

    department = relationship(Department, backref='employees')

    @property
    def full_name(self) -> str:
        """Return the full name of the employee"""
        return f'{self.last_name} {self.first_name} {self.patronymic}'
