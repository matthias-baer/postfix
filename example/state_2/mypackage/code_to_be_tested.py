from postfix import create_function_fixture, create_method_fixture


@create_function_fixture('test_myfunc_happy.pck')
def myfunc(a, b=1, **kwargs):
    return a + b


class MyClass:

    def __init__(self, mystate):
        self.state = mystate

    @create_method_fixture('test_mymethod_invalid_args.pck')
    def mymethod(self, a, *args, **kwargs):
        self.state += 1
        return a + self.state


def run(a, b):
    func_result = myfunc(a, b)
    obj = MyClass(42)
    return obj.mymethod(func_result)
