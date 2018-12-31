from functools import reduce
from datetime import datetime, date, timedelta
from calendar import monthrange
from wpc.model.work import Work
from wpc.repository.crudrepo import CrudRepo


class WorkRepo(CrudRepo):

    def __init__(self, clazz=Work):
        super().__init__(clazz)

    def _q(self, clazz=None):
        """
        Adds to the qyert
        :return: The prepared query object with new filters.
        """
        # TODO: implement clazz logic.
        return super(CrudRepo, self)._q()\
            .filter(Work.customer_id == super()._configurator.customer)\
            .order_by(Work.begin.desc(), Work.end.asc())

    def getAll(self, *criterion):
        return self._q().all()

    def getBetween(self, begin, end):
        return self._q() \
            .filter(Work.begin >= begin) \
            .filter(Work.end <= end) \
            .all()

    def getBetweenStart(self, begin, end):
        """
        :param begin: Lower bound starting date (included in search).
        :param end: Upper bound starting date (excluded from search).
        :return: A list of works between ``begin`` and ``end``, ``end`` excluded.
        """
        return self._q() \
            .filter(Work.begin >= begin) \
            .filter(Work.begin < end) \
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
                (lambda x: (x.price * (x.hours.seconds / 60 / 60)) if x.prod is True else 0),  # TODO: check how this works with non o-clock hours.
                self.getBetweenStart(begin, end + timedelta(days=+1))))

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
                self.getBetweenStart(begin, end + timedelta(days=+1))))

    def getHoursProdBetween(self, begin, end):
        """
        :param begin: Lower bound starting data (included in search).
        :param end: Upper bound starting date (included in search).
        :return: The net for works between ``begin`` and ``end``.
        """
        return reduce(
            (lambda x, y: x + y),
            map(
                (lambda x: x.hours if x.prod is True else 0),
                self.getBetweenStart(begin, end + timedelta(days=+1))))

    def getHoursNonProdBetween(self, begin, end):
        """
        :param begin: Lower bound starting data (included in search).
        :param end: Upper bound starting date (included in search).
        :return: The net for works between ``begin`` and ``end``.
        """
        return reduce(
            (lambda x, y: x + y),
            map(
                (lambda x: x.hours if x.prod is False else 0),
                self.getBetweenStart(begin, end + timedelta(days=+1))))

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
