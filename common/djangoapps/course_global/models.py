from django.db import models

from xmodule_django.models import CourseKeyField

# Create your models here.

class CourseGlobalSetting(models.Model):
  """
  """
  course_id = CourseKeyField(max_length=255, db_index=True, unique=True)
  global_enabled = models.BooleanField(default=True)

  @classmethod
  def all_course_id(cls):
    """
    Returns all of available global course id.
    """
    for cgs in CourseGlobalSetting.objects.filter(global_enabled=True):
      yield cgs.course_id


