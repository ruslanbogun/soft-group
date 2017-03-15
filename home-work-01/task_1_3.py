def decorator(f):
    def wrapper(arg1, arg2, **kwargs):
        try:
            result = f(arg1, arg2, **kwargs)
        except Exception as e:
            print('Exception occurred in', f.__name__, ':', e)
            print('Input args: %s %s' % (arg1, arg2))
            print('Input kwargs:', kwargs)
            result = None
        finally:
            print(result)

    return wrapper


@decorator
def func(x, y, **kwargs):
    return x / y


func(10, 0, op='division', base=10)
func(10, 2, op='division', base=10)
