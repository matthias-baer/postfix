import os
import pickle


class Fixture:

    def save(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)


class FunctionFixture(Fixture):

    def __init__(self, filename, save_dir=None):
        """
        Public constructor for Fixture objects.

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

    def set_state_before(self, state):
        self.pre_state = state

    def set_state_after(self, state):
        self.post_state = state



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
            fixture.set_arguments(args, kwargs)

            # "method" is a method of a class, so args[0] is an instance
            # of the class.
            obj, args = args[0], args[1:]

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