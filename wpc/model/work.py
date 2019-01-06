from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from wpc.model.base import Base


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

    @property
    def datestr(self):
        """
        TODO: write documentation
        :return:
        """
        return self.date.strftime("%d/%m/%Y %H:%M")

    @property
    def beginstr(self):
        return self.begin.strftime("%d/%m/%Y %H:%M")

    @property
    def endstr(self):
        return self.end.strftime("%d/%m/%Y %H:%M")

    @property
    def hours(self):
        return self.end - self.begin
