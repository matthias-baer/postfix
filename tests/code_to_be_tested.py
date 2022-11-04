from postfix.postfix import create_function_fixture


@create_function_fixture('myrecord.pck')
def myfunc(a, b=1, **kwargs):
    return a + b


class MyClass:

    def __init__(self, mystate):
        self.state = mystate

    @create_function_fixture('myrecord.pck')
    def mymethod(self, a, *args, **kwargs):
        return a + self.state

