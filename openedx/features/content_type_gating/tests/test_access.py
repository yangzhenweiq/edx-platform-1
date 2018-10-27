"""
Test audit user's access to various content based on content-gating features.
"""

import ddt
from django.http import Http404
from django.test.utils import override_settings

from courseware.access import has_access
from django.test.client import RequestFactory
from mock import Mock

from student.tests.factories import AdminFactory, CourseEnrollmentFactory, UserFactory

from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory, ItemFactory
from course_modes.tests.factories import CourseModeFactory
from openedx.features.course_duration_limits.config import CONTENT_TYPE_GATING_FLAG
from openedx.core.djangoapps.waffle_utils.testutils import override_waffle_flag

from lms.djangoapps.courseware.module_render import load_single_xblock

@override_settings(FIELD_OVERRIDE_PROVIDERS=(
       'openedx.features.content_type_gating.field_override.ContentTypeGatingFieldOverride',))
@override_waffle_flag(CONTENT_TYPE_GATING_FLAG, True)
@ddt.ddt
class TestProblemTypeAccess(ModuleStoreTestCase):

   def setUp(self):
       self.factory = RequestFactory()
       super(TestProblemTypeAccess, self).setUp()
       self.course = CourseFactory.create(run='testcourse1', display_name='Test Course Title')
       self.audit_mode = CourseModeFactory.create(course_id=self.course.id, mode_slug='audit')
       self.verified_mode = CourseModeFactory.create(course_id=self.course.id, mode_slug='verified')
       self.audit_user = UserFactory.create()
       self.enrollment = CourseEnrollmentFactory.create(user=self.audit_user, course_id=self.course.id, mode='audit')
       with self.store.bulk_operations(self.course.id):
           self.chapter = ItemFactory.create(
               parent=self.course,
               display_name='Overview'
           )
           self.welcome = ItemFactory.create(
               parent=self.chapter,
               display_name='Welcome'
           )
           ItemFactory.create(
               parent=self.course,
               category='chapter',
               display_name='Week 1'
           )
           self.chapter_subsection = ItemFactory.create(
               parent=self.chapter,
               category='sequential',
               display_name='Lesson 1'
           )
           self.chapter_vertical = ItemFactory.create(
               parent=self.chapter_subsection,
               category='vertical',
               display_name='Lesson 1 Vertical - Unit 1'
           )
           self.problem = ItemFactory.create(
               parent=self.chapter_vertical,
               category='problem',
               display_name='Problem - Unit 1 Problem 1',
               graded=True,
           )
           self.dragndrop = ItemFactory.create(
               parent=self.chapter_vertical,
               category='drag-and-drop-v2',
               display_name='Drag Problem - Unit 1 Problem 2',
               graded=True,
           )

   # TODO: Need to add score
   '''@ddt.data(
      (False, False, 0, False),
      (False, True, 0, False),
      (False, False, 1, False),
      (False, True, 1, False),
      (True, False, 0, False),
      (True, True, 0, False),
      (True, False, 1, False),
      (True, True, 1, True),

   )'''
   @ddt.data(
      (False, 0, False),
      (False, 1, False),
      (True, 0, False),
      (True, 1, True),
   )
   @ddt.unpack
   def test_graded_score_weight_values(self, graded, weight, raises):
       problem = ItemFactory.create(parent=self.chapter_vertical,category='problem',display_name='Problem - Unit 1 Problem 1',
                                    graded=graded, weight=weight)
       fake_request = Mock()

       if raises:
         with self.assertRaises(Http404):
            lms_problem = load_single_xblock(fake_request, self.audit_user.id, unicode(self.course.id), unicode(self.problem.scope_ids.usage_id), course=None)
       else:
         # assert an error was not raised
         lms_problem = load_single_xblock(fake_request, self.audit_user.id, unicode(self.course.id), unicode(self.problem.scope_ids.usage_id), course=None)
         self.assertIsNotNone(lms_problem)
