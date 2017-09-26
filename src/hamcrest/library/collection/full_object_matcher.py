from hamcrest.core.base_matcher import BaseMatcher
from tabulate import tabulate

__author__ = "Jon Reid"
__copyright__ = "Copyright 2011 hamcrest.org"
__license__ = "BSD, see License.txt"


class ObjectsMatch(BaseMatcher):

    def __init__(self, obj):
        self.object = obj
        self.incorrect_fields = {}
        self.missing_fields = []
        self.result = {}
        self.difference = set()
        self.extra_fields = set()

    def _matches(self, item):

        if len(item) != len(self.object):
            self.find_missing_fields(item)
        else:
            self.incorrect_fields = {key: [item[key]] for key in item if item[key] != self.object[key]}

        return not self.incorrect_fields and self.difference == set() and self.extra_fields == set()

    # this is the 'expected' block
    def describe_to(self, description):
        if self.extra_fields:
            description.append_text("The following field(s) only to be on the object:\n")
            keys = [key for key in self.object]
            description.append_text(keys)
        elif self.difference:
            description.append_text("The object to have all the following field(s):\n")
            keys = [key for key in self.difference]
            description.append_text(keys)
        elif self.incorrect_fields:
            description.append_text("The following key:value pairs\n")
            required_tabular_format = {key: [self.object[key]] for key in self.incorrect_fields }
            description.append_text(tabulate(required_tabular_format, headers='keys', tablefmt='fancy_grid'))

    # this is the 'but' block
    def describe_mismatch(self, item, mismatch_description):
        if self.extra_fields:
            mismatch_description.append_text("The following field(s) were also on the object:\n")
            keys = [key for key in self.extra_fields]
            mismatch_description.append_text(keys)
        elif self.difference:
            mismatch_description.append_text("The object only has the following fields(s):\n")
            keys = [key for key in item]
            mismatch_description.append_text(keys)
        elif self.incorrect_fields:
            mismatch_description.append_text("\n")
            mismatch_description.append_text(tabulate(self.incorrect_fields, headers='keys', tablefmt='fancy_grid'))


    def find_missing_fields(self, item):
        if len(item) > len(self.object):
            self.find_extra_fields(item)
        else:
            self.difference = set(self.object).difference(set(item))

    def find_extra_fields(self, item):
        self.extra_fields = set(item).difference(set(self.object))

def is_the_same_object(obj):
    """ Matches if every key:value pair matches

    Example:

        object_1 = {
            'name': 'Hammy',
            'age': 7
        }

        object_2 = {
            'name': 'Crest',
            'age': 8
        }
        assert_that(object, is_the_same_object(object_2))

        Produces the following output

        Expected: The following key:value pairs:
        ╒═══════╤════════╕
        │   age │ name   │
        ╞═══════╪════════╡
        │     8 │ Crest  │
        ╘═══════╧════════╛
            but:
        ╒═══════╤════════╕
        │   age │ name   │
        ╞═══════╪════════╡
        │     7 │ Hammy  │
        ╘═══════╧════════╛


        It will also assert that the object passed in has the same exact fields as the object asserting against

        map_1 = {
            'name': 'Jimmy',
            'hobby': 'Surfing',
            'age': 23
        }

        map_2 = {
            'name': 'Jimmy'
        }

        assert_that(map_1, is_the_same_object(map_2))
        AssertionError:
        Expected: The following field(s) only to be on the object:
        ['name']
            but: The following field(s) were also on the object:
        ['hobby', 'age']



    """
    return ObjectsMatch(obj)