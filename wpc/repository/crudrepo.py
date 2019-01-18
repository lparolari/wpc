from .baserepo import BaseRepo
import wpc


class CrudRepo(BaseRepo):

    def create(self, x):
        self._s().add(x)
        self._s().commit()

    def remove(self, x):
        self._s().delete(x).commit()

    def update(self, x):
        self._s().commit()

    def find(self, id_):
        return self._q().filter(wpc.model.Customer.id == id_).first()

    def getAll(self, *criterion):
        return self._q().filter(criterion).all()
