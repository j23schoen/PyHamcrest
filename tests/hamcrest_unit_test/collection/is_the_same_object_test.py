from __future__ import absolute_import

from hamcrest.library.collection.full_object_matcher import *

from hamcrest_unit_test.matcher_test import MatcherTest
from hamcrest import assert_that

__author__ = "Justin Schoen"

class IsTheSameObjectTest(MatcherTest):

    def test_objects_match(self):
        map_1 = {
            'item': 5,
            'value': 1,
            'name': 'Hamcrest'
        }

        map_2 = {
            'item': 5,
            'value': 10,
            'name': 'bill'
        }

        assert_that(map_1, not is_the_same_object(map_2))

    def test_first_object_has_additional_fields(self):
        map_1 = {
            'name': 'Jimmy',
            'hobby': 'Surfing',
            'age': 23
        }

        map_2 = {
            'name': 'Jimmy'
        }

        assert_that(map_1, not is_the_same_object(map_2))

    def test_second_object_has_additional_fields(self):
        map_1 = {
            'name': 'Jimmy'
        }
        map_2 = {
            'name': 'Jimmy',
            'hobby': 'Surfing',
            'age': 23
        }

        assert_that(map_1, not is_the_same_object(map_2))
