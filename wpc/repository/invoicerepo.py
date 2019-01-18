from .crudrepo import CrudRepo
import wpc

from sqlalchemy import func, and_


class InvoiceRepo(CrudRepo):

    def __init__(self, clazz=wpc.model.Invoice):
        super().__init__(clazz)

    def _q(self, clazz=None):
        q = super(CrudRepo, self)._q(clazz)

        if clazz is None:
            q = q.filter(wpc.model.Invoice.customer_id == super()._configurator.customer)
            q = q.order_by(wpc.model.Invoice.emitted_at.desc(), wpc.model.Invoice.from_dt.desc())

        return q

    # def _q_def(self):
    #    return self._q()\
    #        .filter(Invoice.customer_id == super()._configurator.customer)\
    #        .order_by(Invoice.emitted_at.desc(), Invoice.from_dt.desc())

    def getAll(self, *criterion):
        return self._q().all()

    def getAllWithHours(self):
        return self._q(wpc.model.InvoiceWithHours) \
            .filter(wpc.model.InvoiceWithHours.customer_id == super()._configurator.customer) \
            .order_by(wpc.model.InvoiceWithHours.emitted_at.desc(), wpc.model.InvoiceWithHours.from_dt.desc())\
            .all()

    def getEmittedBetweenWithHours(self, begin, end):
        return self._q(wpc.model.InvoiceWithHours) \
            .filter(wpc.model.InvoiceWithHours.customer_id == super()._configurator.customer) \
            .filter(wpc.model.InvoiceWithHours.emitted_at >= begin) \
            .filter(wpc.model.InvoiceWithHours.emitted_at <= end) \
            .order_by(wpc.model.InvoiceWithHours.emitted_at.desc(), wpc.model.InvoiceWithHours.from_dt.desc())\
            .all()

    def getNextProg(self):
        max_ = self._q().with_entities(func.max(wpc.model.Invoice.prog).label('max')).first().max
        max_ = max_ if max_ is not None else 0
        return max_ + 1
