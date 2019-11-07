class Function:

    def __init__(self, fun, args, kwargs):
        self._fun = fun
        self._args = args
        self._kwargs = kwargs

    def __call__(self, *args, **kwargs):
        if self._args is None and self._kwargs is None:
            return self._fun(*args, **kwargs)
        if self._kwargs is None:
            return self._fun(*self._args, *args, **kwargs)
        if self._args is None:
            return self._fun(*args, **self._kwargs, **kwargs)
        else:
            return self._fun(*self._args, *args, **self._kwargs, **kwargs)

    @property
    def fun(self):
        return self._fun

    @fun.setter
    def fun(self, value):
        if callable(value):
            self._fun = value
        else:
            raise TypeError("'{}' is not callable".format(type(value)))

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        if type(value) is list:
            self._args = value
        else:
            raise TypeError("'{}' is not list".format(type(value)))

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, value):
        if type(value) is dict:
            self._kwargs = value
        else:
            raise TypeError("'{}' is not dict".format(type(value)))