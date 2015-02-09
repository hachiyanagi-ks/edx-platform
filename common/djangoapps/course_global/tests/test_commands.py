from django.test import TestCase
from django.core.management import call_command
from django.utils.six import StringIO

from xmodule.modulestore.tests.factories import CourseFactory
from student.tests.factories import UserFactory, UserStandingFactory, CourseEnrollmentFactory
from student.models import CourseEnrollment, UserStanding

from course_global.models import CourseGlobalSetting
from course_global.tests.factories import CourseGlobalSettingFactory

class EnrollAllUsersTest(TestCase):

    def setUp(self):
        self.users = [UserFactory.create() for _ in range(5)]
        self.courses = [CourseFactory.create(display_name = "test course {}".format(i)) for i in range(3)]
        # course0 and course1 are global course
        CourseGlobalSettingFactory.create(course_id = self.courses[0].id)
        CourseGlobalSettingFactory.create(course_id = self.courses[1].id)

    def test_enroll_all_users(self):
        active_users = [self.users[0], self.users[1], self.users[3], self.users[4]]
        # mark user2 resigned
        UserStandingFactory.create(user = self.users[2], account_status = UserStanding.ACCOUNT_DISABLED, changed_by = self.users[0])

        # user0 is enroll in course0
        CourseEnrollment.enroll(self.users[0], self.courses[0].id)
        # user1 is enroll in course0 and course1
        CourseEnrollment.enroll(self.users[1], self.courses[0].id)
        CourseEnrollment.enroll(self.users[1], self.courses[1].id)

        self.assertEquals(2, CourseEnrollment.num_enrolled_in(self.courses[0].id))
        self.assertEquals(1, CourseEnrollment.num_enrolled_in(self.courses[1].id))

        call_command('enroll_global_course')

        self.assertEquals(4, CourseEnrollment.num_enrolled_in(self.courses[0].id))
        self.assertEquals(4, CourseEnrollment.num_enrolled_in(self.courses[1].id))

        for user in active_users:
            self.assertEquals(2, CourseEnrollment.enrollments_for_user(user).count())

