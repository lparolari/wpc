from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class Payment(Base):

    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, autoincrement=True)

    paid_at = Column(DateTime, nullable=False, default=datetime.today())

    gross = Column(Float)
    tax = Column(Float)
    net = Column(Float, nullable=False)

    note = Column(String)

    # foreign key to customers.
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("Customer", foreign_keys=[customer_id])

    # foreign key to invoices.
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    invoice = relationship("Invoice", foreign_keys=[invoice_id])

    def __repr__(self) -> str:
        return '<{0}.{1} #{2} :: net:{3}>'.format(self.__module__, type(self).__name__, self.id, self.net)

    @property
    def paid_at_str(self):
        """
        :return: A string representation for *paid_at* date.
        """
        return self.paid_at.strftime("%d/%m/%Y %H:%M")
