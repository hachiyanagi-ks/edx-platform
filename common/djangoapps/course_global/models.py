from django.db import models

from xmodule_django.models import CourseKeyField

# Create your models here.

class CourseGlobalSetting(models.Model):
  """
  """
  course_id = CourseKeyField(max_length=255, db_index=True, unique=True)
  global_enabled = models.BooleanField(default=True)

