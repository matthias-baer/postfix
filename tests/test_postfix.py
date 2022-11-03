import os.path
import unittest

from postfix import Fixture
from tests.code_to_be_tested import myfunc, MyClass


class TestCreateFixture(unittest.TestCase):

    def tearDown(self):
        os.remove('myrecord.pck')

    def test_record_myfunc_explicit_args(self):
        result = myfunc(1, 2)
        self.assertTrue(os.path.exists('myrecord.pck'))

        fixture = Fixture.from_file('myrecord.pck')
        self.assertEqual(result, fixture.return_value)
        self.assertEqual(3, fixture.return_value)

    def test_record_mymethod_explicit_args(self):
        obj = MyClass(42)
        result = obj.mymethod(1, 2)

        self.assertTrue(os.path.exists('myrecord.pck'))

        fixture = Fixture.from_file('myrecord.pck')
        self.assertEqual(result, fixture.return_value)
        self.assertEqual(43, fixture.return_value)