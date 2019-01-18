from .crudrepo import CrudRepo
import wpc


class CustomerRepo(CrudRepo):

    def __init__(self, clazz=wpc.model.Customer):
        super().__init__(clazz)
