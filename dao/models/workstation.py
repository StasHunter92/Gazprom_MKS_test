from sqlalchemy import Column, Integer, String

from dao.models.base_model import Base


# ----------------------------------------------------------------------------------------------------------------------
class Workstation(Base):
    __tablename__ = 'workstations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)
    ip_address = Column(String(15), unique=True)
    mac_address = Column(String(17), unique=True)
