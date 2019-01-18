from functools import reduce
from datetime import datetime, date, timedelta
from calendar import monthrange

# TODO: questi import relativi sono necessari perche' il primo __init__.py del package wpc
#  effettua l'importazione dei subpackage in dato ordine, e se alcuni moduli, come questo,
#  si riferiscono a classi o funzioni dello stesso livello, dello stesso subpackage,
#  l' "import wpc" generico non funziona perche' per python questo subpackage non e' stato
#  ancora inizializzato completamente ed inserito nel dizionario.

from .crudrepo import CrudRepo

# TODO: questo import relativo si evita con il seguente "import wpc":
#  from ..config.configurator import Configurator
#  Ma funziona solo se wpc.config e' stato gia' correttamente inzializzato

import wpc


class WorkRepo(CrudRepo):

    # TODO: l'eliminazione dell'import relativo di cui sopra richiede ora
    #  un riferimeno "FQDN"
    _configurator = wpc.config.Configurator()

    def __init__(self, clazz=wpc.model.Work):
        super().__init__(clazz)

    def _q(self, clazz=None):
        """
        Adds to the qyert
        :return: The prepared query object with new filters.
        """
        # TODO: implement clazz logic.
        return super(CrudRepo, self)._q()\
            .filter(wpc.model.Work.customer_id == super()._configurator.customer)\
            .order_by(wpc.model.Work.begin.desc(), wpc.model.Work.end.asc())

    def getAll(self, *criterion):
        return self._q().all()

    def getBetween(self, begin, end):
        return self._q() \
            .filter(wpc.model.Work.begin >= begin) \
            .filter(wpc.model.Work.end <= end) \
            .all()

    def getBetweenStart(self, begin, end):
        """
        :param begin: Lower bound starting date (included in search).
        :param end: Upper bound starting date (excluded from search).
        :return: A list of works between ``begin`` and ``end``, ``end`` excluded.
        """
        return self._q() \
            .filter(wpc.model.Work.begin >= begin) \
            .filter(wpc.model.Work.begin < end) \
            .all()

    def getProfitGrossBetween(self, begin, end):
        """
        :param begin: Lower bound starting data (included in search).
        :param end: Upper bound starting date (included in search).
        :return: The gross for works between ``begin`` and ``end``.
        """
        return reduce(
            (lambda x, y: x + y),
            map(
                (lambda x: (
                    (x.price * (x.hours.seconds / 60 / 60)) if x.prod is True else 0)
                 ),  # TODO: check how this works with non o-clock hours.
                self.getBetweenStart(begin, end + timedelta(days=+1))), 0)

    def getHoursBetween(self, begin, end):
        """
        :param begin: Lower bound starting data (included in search).
        :param end: Upper bound starting date (included in search).
        :return: The hours of work between ``begin`` and ``end``.
        """
        return reduce(
            (lambda x, y: x + y),
            map(
                (lambda x: x.hours),
                self.getBetweenStart(begin, end + timedelta(days=+1))), 0)

    def getHoursProdBetween(self, begin, end):
        """
        :param begin: Lower bound starting data (included in search).
        :param end: Upper bound starting date (included in search).
        :return: The net for works between ``begin`` and ``end``.
        """
        return reduce(
            (lambda x, y: x + y),
            map(
                (lambda x: x.hours if x.prod is True else timedelta(0)),
                self.getBetweenStart(begin, end + timedelta(days=+1))), 0)

    def getHoursNonProdBetween(self, begin, end):
        """
        :param begin: Lower bound starting data (included in search).
        :param end: Upper bound starting date (included in search).
        :return: The net for works between ``begin`` and ``end``.
        """
        return reduce(
            (lambda x, y: x + y),
            map(
                (lambda x: x.hours if x.prod is False else timedelta(0)),
                self.getBetweenStart(begin, end + timedelta(days=+1))), 0)

    def getKmBetween(self, begin, end):
        """
        :param begin: Lower bound starting data (included in search).
        :param end: Upper bound starting date (included in search).
        :return: The km for works between ``begin`` and ``end``.
        """
        return reduce(
            (lambda x, y: x + y),
            map(
                (lambda x: x.km),
                self.getBetweenStart(begin, end + timedelta(days=+1))), 0)

    # not core methods: utilize other methods for the result.

    def getByYear(self, year=date.today().year):
        """
        :param year: Target year.
        :return: A list of works between January 1 and December 31 ``year``.
        """
        begin = date(year, 1, 1)
        end = date(year, 12, 31) + timedelta(days=+1)
        return self.getBetweenStart(begin, end)

    def getByMonth(self, month=date.today().month, year=date.today().year):
        """
        :param month: Target month.
        :param year: Target year.
        :return: A list of works between first and last (included) of ``month`` in ``year``.
        """
        begin = date(year, month, 1)
        end = date(year, month, monthrange(year, month)[1]) + timedelta(days=+1)
        return self.getBetweenStart(begin, end)

    def getByDay(self, day=date.today().day, month=date.today().month, year=date.today().year):
        """
        :param day: Target day.
        :param month: Target month.
        :param year: Target year.
        :return: A list of works between in ``day`` of ``month`` in ``year``.
        """
        begin = date(year, month, day)
        end = begin + timedelta(1)
        return self.getBetweenStart(begin, end)

    def getProfitTaxBetween(self, begin, end):
        """
        :param begin: Lower bound starting data (included in search).
        :param end: Upper bound starting date (included in search).
        :return: The tax for works between ``begin`` and ``end``.
        """
        return self.getProfitGrossBetween(begin, end) / 100 * 20

    def getProfitNetBetween(self, begin, end):
        """
        :param begin: Lower bound starting data (included in search).
        :param end: Upper bound starting date (included in search).
        :return: The net for works between ``begin`` and ``end``.
        """
        return self.getProfitGrossBetween(begin, end) - self.getProfitTaxBetween(begin, end)

    def getTotalTaxBetween(self, begin, end):
        """
        :param begin: Lower bound starting data (included in search).
        :param end: Upper bound starting date (included in search).
        :return: The tax for works between ``begin`` and ``end``.
        """
        return (self.getProfitGrossBetween(begin, end) + self.getKmBetween(begin, end) / self._configurator.km_litre * self._configurator.oil_cost_litre) / 100 * 20

    def getTotalGrossBetween(self, begin, end):
        """
        :param begin: Lower bound starting data (included in search).
        :param end: Upper bound starting date (included in search).
        :return: The gross for works between ``begin`` and ``end``.
        """
        return self.getProfitGrossBetween(begin, end) + self.getKmBetween(begin, end) / self._configurator.km_litre * self._configurator.oil_cost_litre

    def getTotalNetBetween(self, begin, end):
        """
        :param begin: Lower bound starting data (included in search).
        :param end: Upper bound starting date (included in search).
        :return: The net for works between ``begin`` and ``end``.
        """
        return self.getTotalGrossBetween(begin, end) - self.getTotalTaxBetween(begin, end)
