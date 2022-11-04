import os.path
import unittest

from postfix import Fixture
from mypackage.code_to_be_tested import myfunc, MyClass


class TestBase(unittest.TestCase):
    fixture_path = os.path.join(os.path.abspath(__file__), 'fixtures')

    def load_fixture(self, filename):
        return Fixture.from_file(os.path.join(self.fixture_path, filename))


class TestMyFunction(TestBase):

    def test_happy_path(self):
        fixture = self.load_fixture('test_myfunc_happy.pck')
        a, b = fixture.args
        actual = myfunc(a, b)
        self.assertEqual(fixture.return_value, actual)


class TestMyClass(TestBase):

    def test_mymethod_invalid_args(self):
        fixture = self.load_fixture('test_mymethod_invalid_args.pck')
        a, b = fixture.args
        obj = fixture.pre_state
        actual = obj.mymethod(a)
        self.assertEqual(fixture.return_value, actual)
        # Optionally: do assertions on fixture.post_state
        ...


if __name__ == '__main__':
    unittest.main()
