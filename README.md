# postfix

A Python package to facilitate writing tests for a testless code base.

## Installation

```
pip install --upgrade postfix
```

## Usage

Suppose you have some tremendously complex code, but no tests for that
code. But you are sufficiently convinced, that right now, it's working
as it should. You want to do some refactoring, but you don't dare to do so 
without tests (wise decision!). So you decide to write tests a posteriori
to make sure that after refactoring, the code works as before. Let's 
suppose that we want
to create tests for the function `myfunc` and the method `MyClass.mymethod`
(see `example/state_1`). And let's suppose that it is complicated
to get realistic data for the arguments of that function/method. In order
to quickly get a first test coverage with realistic input and output data, 
we will use `postfix` to create test fixtures. Annotate the function or
method for which you create a fixture with the decorator `postfix.create_fixture`
(see `example/state2`) and run your code. Remove the decorators from the production
code, move the dumped fixture files to
your newly created test suite directory and use them to write tests (see
`examples/state_3`).

### Limitations

In *postfix* you cannot instrument methods or functions that are located
in the main module. However, for any nontrivial project with more than
one Python file this should not be a limitation.
