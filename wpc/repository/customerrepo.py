from wpc.repository.crudrepo import CrudRepo
from wpc.model.customer import Customer


class CustomerRepo(CrudRepo):

    def __init__(self, clazz=Customer):
        super().__init__(clazz)
