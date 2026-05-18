from django.db import models


class DropdownItem:
    def get_key(self):
        raise NotImplementedError

    def get_value(self):
        raise NotImplementedError


class BaseModel(models.Model):

    def to_json(self):
        data = {}
        return data

    class Meta:
        abstract = True


# Create your models here.
class Role(DropdownItem, models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def get_key(self):
        return self.id

    def get_value(self):
        return self.name

    class Meta:
        db_table = "sos_role"


class User(DropdownItem, models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    login = models.EmailField()
    password = models.CharField(max_length=20)
    dob = models.DateField(max_length=20)
    gender = models.CharField(max_length=50, default='')
    mobile_number = models.CharField(max_length=50, default='')
    role_id = models.IntegerField()
    role_name = models.CharField(max_length=50)
    photo = models.CharField(max_length=200, blank=True, default="")

    def get_key(self):
        return self.id

    def get_value(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "sos_user"


class College(DropdownItem, models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)

    def get_key(self):
        return self.id

    def get_value(self):
        return self.name

    class Meta:
        db_table = "sos_college"


class Course(DropdownItem, models.Model):
    name = models.CharField(max_length=50)
    duration = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    college_id = models.IntegerField(default=0)
    college_name = models.CharField(max_length=50, default="")

    def get_key(self):
        return self.id

    def get_value(self):
        return self.name

    class Meta:
        db_table = "sos_course"


class Faculty(DropdownItem, models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=20)
    address = models.CharField(max_length=50)

    college_id = models.IntegerField()
    college_name = models.CharField(max_length=50)

    subject_id = models.IntegerField()
    subject_name = models.CharField(max_length=50)

    course_id = models.IntegerField()
    course_name = models.CharField(max_length=50)

    def get_key(self):
        return self.id

    def get_value(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "sos_faculty"


class Marksheet(DropdownItem, models.Model):
    roll_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    physics = models.IntegerField()
    chemistry = models.IntegerField()
    maths = models.IntegerField()
    year = models.IntegerField()
    student_id = models.IntegerField()

    def get_key(self):
        return self.id

    def get_value(self):
        return f"{self.name} - {self.roll_number}"

    @property
    def total(self):
        return self.physics + self.chemistry + self.maths

    @property
    def percentage(self):
        return round((self.total / 300) * 100, 2)

    class Meta:
        db_table = "sos_marksheet"


class Student(DropdownItem, models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    dob = models.DateField(null=True, blank=True)
    mobile_number = models.CharField(max_length=20)

    college_id = models.IntegerField()
    college_name = models.CharField(max_length=50)

    def get_key(self):
        return self.id

    def get_value(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "sos_student"


class Subject(DropdownItem, models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    course_id = models.IntegerField()
    course_name = models.CharField(max_length=50)

    def get_key(self):
        return self.id

    def get_value(self):
        return self.name

    class Meta:
        db_table = "sos_subject"


class TimeTable(DropdownItem, models.Model):
    exam_date = models.DateField()
    exam_time = models.CharField(max_length=50)

    semester = models.CharField(max_length=50)

    course_id = models.IntegerField()
    course_name = models.CharField(max_length=50)

    subject_id = models.IntegerField()
    subject_name = models.CharField(max_length=50)

    def get_key(self):
        return self.id

    def get_value(self):
        return (
            f"{self.course_name} - "
            f"{self.subject_name} - "
            f"{self.exam_date} {self.exam_time}"
        )

    class Meta:
        db_table = "sos_timetable"
