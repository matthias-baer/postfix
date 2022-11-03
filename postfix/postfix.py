import os
import pickle

__all__ = ['Fixture', 'create_fixture']


class Fixture:

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
        self.args = None
        self.kwargs = None
        self.return_value = None

    def set_arguments(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs

    def set_state_after(self, state):
        self.post_state = state

    def set_return(self, value):
        self.return_value = value

    def save(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)


def create_fixture(filename):
    """Decorator for temporary code instrumentation for creating test fixtures."""

    def decorator(func):
        def inner(*args, **kwargs):
            fixture = Fixture(filename)
            fixture.set_arguments(args, kwargs)

            result = func(*args, **kwargs)

            # If "func" is a method of a class, then args[0] is an instance
            # of the class. The method could alter the state of the instance,
            # so also save that state in the fixture:
            if len(args) > 0:
                fixture.set_state_after(args[0])

            fixture.set_return(result)
            fixture.save()
            return result

        return inner

    return decorator
