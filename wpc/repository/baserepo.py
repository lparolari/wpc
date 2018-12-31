from wpc.db.db import Db
from wpc.config.configurator import Configurator


class BaseRepo(object):
    _db = Db()
    _clazz = None
    _configurator = Configurator()

    def __init__(self, clazz):
        """
        BaseRepo Constructor. Initializes the repository with the utilizer model.
        :param clazz: The repo utilizer model class.
        """
        self._clazz = clazz

    def _q(self, clazz=None):
        """
        :return: The query instanced with the utilizer model class.
        """
        return self._db.session.query(clazz if clazz is not None else self._clazz)

    def _s(self):
        """
        :return: A session.
        """
        return self._db.session

    def query(self):
        """
        :return: A blank query.
        """
        return self._q()


