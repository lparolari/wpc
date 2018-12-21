from sqlalchemy import Column, Integer, String
from wpc.model.base import Base


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
