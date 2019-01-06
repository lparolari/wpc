from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from wpc.model.base import Base


class InvoiceWithHours(Base):

    __tablename__ = 'invoices_with_hours'

    id = Column(Integer, primary_key=True, autoincrement=True)

    emitted_at = Column(DateTime, nullable=False, default=datetime.today())

    gross = Column(Float)
    tax = Column(Float)
    net = Column(Float)

    from_dt = Column(DateTime, nullable=False)
    to_dt = Column(DateTime, nullable=False)

    reason = Column(String, nullable=False)
    prog = Column(Integer, nullable=False)

    note = Column(String)

    hours_prod = Column(Float, default=0, nullable=False)
    hours_non_prod = Column(Float, default=0, nullable=False)

    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("Customer", foreign_keys=[customer_id])

    @property
    def emitted_at_str(self):
        return self.emitted_at.strftime("%d/%m/%Y %H:%M")

    @property
    def from_dt_str(self):
        return self.from_dt.strftime("%d/%m/%Y %H:%M")

    @property
    def to_dt_str(self):
        return self.to_dt.strftime("%d/%m/%Y %H:%M")

    def __repr__(self) -> str:
        return '<{0}.{1}:  {2}>'.format(self.__module__, type(self).__name__, self.id)

