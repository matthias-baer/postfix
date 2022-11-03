def myfunc(a, b=1, **kwargs):
    return a + b


class MyClass:

    def __init__(self, mystate):
        self.state = mystate

    def mymethod(self, a, *args, **kwargs):
        self.state += 1
        return a + self.state


def run(a, b):
    func_result = myfunc(a, b)
    obj = MyClass(42)
    return obj.mymethod(func_result)


if __name__ == '__main__':
    run(1, 2)
