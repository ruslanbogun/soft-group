class MyList:
    list = []

    def __init__(self, arg):
        self.list = arg

    def flatMap(self):
        def rec(h, t):
            for i in t:
                if isinstance(i, int):
                    h.append(i)
                else:
                    rec(h, i)
            return h

        return rec([], self.list)


l = [1, 2, 3, [4, 5, [6, 7]]]

print(MyList(l).flatMap())
