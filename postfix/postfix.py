import os
import pickle
from copy import deepcopy


class Fixture:

    def save(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def from_file(cls, filename):
        """Loads a fixture from file."""
        with open(filename, 'rb') as file:
            return pickle.load(file)


class FunctionFixture(Fixture):
    """A class for dumping and loading data entering and leaving a Python function."""

    def __init__(self, filename, save_dir=None):
        """
        Public constructor.

        Parameters
        ----------
        filename:   str
            File name for saving fixture to file system.
        save_dir:   str, default: None
            Specifies save directory. Default: current directory.
        """
        self.filename = filename
        self.save_dir = save_dir or os.path.curdir

    def set_arguments(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs

    def set_return(self, value):
        self.return_value = value


class MethodFixture(FunctionFixture):
    """A class for dumping and loading data used by a method.

        MethodFixture objects not only store the data entering and leaving
        the method, but also the state of the object containing the
        method before and after execution.
    """

    def __init__(self, filename, save_dir=None):
        super(MethodFixture, self).__init__(filename, save_dir)
        self._pre_state = None
        self._post_state = None

    def set_state_before(self, state):
        self._pre_state = state

    def set_state_after(self, state):
        self._post_state = state

    @property
    def pre_state(self):
        """Returns the instance before executing the method."""

        # Return a *copy*, because otherwise the object may be altered when
        # calling methods on it and one couldn't compare with the actual
        # state before execution any more.
        return deepcopy(self._pre_state)

    @property
    def post_state(self):
        """Returns the instance after executing the method."""
        return self._pre_state


def create_function_fixture(filename):
    """Decorator for temporary function instrumentation for creating test fixtures.

       Do not use this for methods! Use create_method_fixture instead.
    """

    def decorator(func):
        def inner(*args, **kwargs):
            fixture = FunctionFixture(filename)
            fixture.set_arguments(args, kwargs)

            result = func(*args, **kwargs)

            fixture.set_return(result)
            fixture.save()
            return result

        return inner

    return decorator


def create_method_fixture(filename):
    """Decorator for temporary method instrumentation for creating test fixtures."""

    def decorator(method):
        def inner(*args, **kwargs):
            fixture = MethodFixture(filename)

            # "method" is a method of a class, so args[0] is an instance
            # of the class.
            obj, args = args[0], args[1:]
            fixture.set_arguments(args, kwargs)

            # The workings of the method could depend on the
            # current state of the object. So we need to save it, too:
            fixture.set_state_before(obj)

            result = method(obj, *args, **kwargs)

            # The method could also alter the state of the instance,
            # so we save that state in the fixture:
            fixture.set_state_after(obj)

            fixture.set_return(result)
            fixture.save()
            return result

        return inner

    return decorator
