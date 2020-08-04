class Const(object):
    def __setattr__(self, name, val):
        if name in self.__dict__:
            raise TypeError("Constant can not be modified.")

        if not name.isupper():
            raise TypeError("Constant name must be in upper case.")

        super().__setattr__(name, val)


import sys

sys.modules[__name__] = Const()
