from typing import Tuple
from .function import Function


class GreaterThanZero:

    def __init__(self, name):
        self.name = name

    def __set_name__(self, owner, name):
        if not hasattr(self, 'name'):
            self.name = name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError(self.name + ' cannot be lower than zero!')
        setattr(instance, self.name, value)


class Validated:
    def __init__(self, name, valid):
        self.name = name
        self.valid = valid

    def __set_name__(self, owner, name):
        if not hasattr(self, 'name'):
            self.name = name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if value not in self.valid:
            raise ValueError(str(value) + ' has to have one of ' + str(self.valid))
        setattr(instance, self.name, value)


class FuncDescriptor:

    def __init__(self, *args, **kwargs) -> None:
        self._args = args
        self._kwargs = kwargs

    def __get__(self, instance, owner) -> Function:
        try:
            fun = instance.__dict__[self.name]
        except KeyError:
            return lambda *args, **kwargs: NotImplementedError("Called not implemented function with name {}")
        return fun

    def __set__(self, instance, value: Tuple[callable, list, dict]) -> None:
        try:
            fun = instance.__dict__[self.name]
        except KeyError:
            fun = Function(None, None, None)
        finally:
            if callable(value):
                fun.fun = value
            else:
                for element in value:
                    if type(element) is dict:
                        for key, value in iter(self._kwargs):
                            if key not in element.keys():
                                element[key] = value
                        fun.kwargs = element
                    elif type(element) is list:
                        fun.args = element + list(self._args)
                    elif callable(element):
                        fun.fun = element

            instance.__dict__[self.name] = fun

    def __set_name__(self, owner, name: str) -> None:
        self.name = name

    @staticmethod
    def not_implement(name: str) -> None:
        raise NotImplementedError("Function at {} has not been set".format(name))



def test_fun(*args, **kwargs):
    print(*args)


class Mock:
    fun = FuncDescriptor(test_fun, ["default"], {'t': None})

    def __init__(self, fun=print, args='test'):
        self.fun = test_fun, ["default"], {'t': None}
        pass


if __name__ == '__main__':
    a = Mock()
    a.fun()
    # b = Mock()
    # a.fun = test_fun, ["a"], {'test': None}
    # a.fun()
    # # b.fun = (test_fun, ["b"], {'test': None})
    # c = a.fun
    # a.fun = (test_fun, ["c"], {'test': None})
    # a.fun()
    # c()
    # c = (test_fun, ["b"], {'test': None})
    # c()
    # a.fun()
    # a = FuncDescriptor()
    # a = print, ['ok'], {}
    # a()
    # print('ok')
