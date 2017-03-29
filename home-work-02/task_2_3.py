class PublicMeta(type):
    def __new__(mcs, name, bases, attrs):

        pattern = "_" + name + "__"

        def pretty_func():
            print('Some useful message')

        def do_things(self):
            print(self.var)

        def rename_attributes(key, value):
            return key.replace(pattern, "") if not callable(value) else key

        new_dct = {rename_attributes(key, value): value for key, value in attrs.items()}

        new_dct.update({'pretty_func': staticmethod(pretty_func)})
        new_dct.update({'do_things': do_things})

        return type.__new__(mcs, name, bases, new_dct)


class A(metaclass=PublicMeta):
    __var = 10

    def __init__(self, x):
        self.x = x


a = A(10)
print(a.var)

a.pretty_func()

a.do_things()

A(10).pretty_func()
