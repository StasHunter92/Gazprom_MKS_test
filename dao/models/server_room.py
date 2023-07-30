from sqlalchemy import Column, Integer

from dao.models.base_model import Base


# ----------------------------------------------------------------------------------------------------------------------
class ServerRoom(Base):
    __tablename__ = 'server_rooms'

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, unique=True)
