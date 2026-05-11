from django.db.models import Max
from service.models import Role
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService

'''
It contains Role business logics.   
'''


class RoleService(BaseService):

    def search(self, params):

        page_no = max(1, int(params.get("pageNo", 1)))
        page_size = self.pageSize

        start = (page_no - 1) * page_size
        end = start + page_size

        q = self.get_model().objects.all()

        name = params.get("name")
        if DataValidator.isNotNull(name):
            q = q.filter(name__istartswith=name.strip())

        description = params.get("description")
        if DataValidator.isNotNull(description):
            q = q.filter(description__istartswith=description.strip())

        q = q[start:end]

        last_role = Role.objects.last()

        params["maxId"] = q.aggregate(Max("id"))["id__max"] or 0
        params["lastId"] = last_role.id if last_role else 0
        params["index"] = start

        return q

    def get_model(self):
        return Role
