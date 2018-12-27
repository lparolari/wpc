from wpc.repository.crudrepo import CrudRepo
from wpc.model.work import Work
from datetime import datetime, date, timedelta
from calendar import monthrange


class WorkRepo(CrudRepo):
    def _q(self):
        """
        Adds to the qyert
        :return: The prepared query object with new filters.
        """
        return super(CrudRepo, self)._q().order_by(Work.begin.desc(), Work.end.asc())

    def getAll(self, *criterion):
        return self._q().all()

    def getBetween(self, begin, end):
        return self._q() \
            .filter(Work.begin >= begin) \
            .filter(Work.end <= end) \
            .all()

    def getBetweenStart(self, begin, end):
        return self._q() \
            .filter(Work.begin >= begin) \
            .filter(Work.begin < end) \
            .all()

    def getByYear(self, year=date.today().year):
        begin = date(year, 1, 1)
        end = date(year, 12, 31)
        return self.getBetweenStart(begin, end)

    def getByMonth(self, month=date.today().month, year=date.today().year):
        begin = date(year, month, 1)
        end = date(year, month, monthrange(year, month)[1])
        return self.getBetweenStart(begin, end)

    def getByDay(self, day=date.today().day, month=date.today().month, year=date.today().year):
        begin = date(year, month, day)
        end = begin + timedelta(1)
        return self.getBetweenStart(begin, end)
