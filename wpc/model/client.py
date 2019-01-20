from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    note = Column(String)

    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("Customer", foreign_keys=[customer_id])
