from service.models import TimeTable
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.core.paginator import Paginator

'''
It contains Role business logics.   
'''


class TimeTableService(BaseService):

    def search(self, params):

        page_no = int(params.get("page_no", 0))
        page_size = self.pageSize

        query = self.get_model().objects.all()

        if page_no == 0:
            return query

        value = params.get("exam_date", None)
        if DataValidator.isNotNull(value):
            query = query.filter(exam_date__istartswith=value.strip())

        value = params.get("exam_time", None)
        if DataValidator.isNotNull(value) and str(value) != "0":
            query = query.filter(exam_time__istartswith=value.strip())

        value = params.get("semester", None)
        if DataValidator.isNotNull(value) and str(value) != "0":
            query = query.filter(semester__istartswith=value.strip())

        value = params.get("course_id", None)
        if DataValidator.isNotNull(value) and str(value) != "0":
            query = query.filter(course_id=value)

        value = params.get("subject_id", None)
        if DataValidator.isNotNull(value) and str(value) != "0":
            query = query.filter(subject_id=value)

        paginator = Paginator(query, page_size)

        page_obj = paginator.get_page(page_no)

        params["has_next"] = page_obj.has_next()
        params["has_previous"] = page_obj.has_previous()
        params["start_index"] = (page_no - 1) * page_size

        return page_obj

    def get_model(self):
        return TimeTable
