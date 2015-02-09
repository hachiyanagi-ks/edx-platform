from django.core.management.base import BaseCommand

from django.contrib.auth.models import User

from student.models import UserStanding, CourseEnrollment
from course_global.models import CourseGlobalSetting

from course_global.management.commands import users_unenrolled_in

class Command(BaseCommand):
    """
    Enroll all users to all global courses.
    """

    def handle(self, *args, **options):
        for global_course_id in CourseGlobalSetting.all_course_id():
            for user in users_unenrolled_in(global_course_id):
                CourseEnrollment.enroll(user, global_course_id)
