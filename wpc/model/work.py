from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from .base import Base


class Work(Base):
    __tablename__ = 'works'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False)
    begin = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    minutes = Column(Integer)
    add = Column(Float)
    note = Column(String)
    registry = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    prod = Column(Boolean, nullable=False, default=True)
    km = Column(Integer, nullable=False, default=0)

    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("Customer", foreign_keys=[customer_id])

    client_id = Column(Integer, ForeignKey("clients.id"))
    client = relationship("Client", foreign_keys=[client_id])

    def __repr__(self) -> str:
        return '<{0}.{1} #{2} :: registry:{3}>'.format(self.__module__, type(self).__name__, self.id, self.registry)

    @property
    def datestr(self):
        """
        :return: A string representation for *date* date.
        """
        return self.date.strftime("%d/%m/%Y %H:%M")

    @property
    def beginstr(self):
        """
        :return: A string representation for *begin* date.
        """
        return self.begin.strftime("%d/%m/%Y %H:%M")

    @property
    def endstr(self):
        """
        :return: A string representation for *end* date.
        """
        return self.end.strftime("%d/%m/%Y %H:%M")

    @property
    def hours(self):
        """
        :return: The difference between end and begin, i.e., number of
            worker hours.
        """
        return self.end - self.begin
