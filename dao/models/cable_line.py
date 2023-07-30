from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from dao.models.base_model import Base
from dao.models.employee import Employee
from dao.models.workstation import Workstation


# ----------------------------------------------------------------------------------------------------------------------
class CableLine(Base):
    __tablename__ = 'cable_lines'

    id = Column(Integer, primary_key=True, index=True)
    socket_number = Column(Integer)
    port_number_socket = Column(Integer)
    port_number_patch_panel = Column(Integer)
    length = Column(Integer)

    employee_id = Column(Integer, ForeignKey('employees.id'), index=True)
    employee = relationship(Employee, backref='cable_lines')

    workstation_id = Column(Integer, ForeignKey('workstations.id'), index=True)
    workstation = relationship(Workstation, backref='cable_lines')
