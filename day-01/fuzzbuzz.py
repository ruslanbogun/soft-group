def f():
    for n in range(1, 101):
        if n % 3 == 0 and n % 5:
            print("fizzbuzz")
        elif n % 3 == 0:
            print("fizz")
        elif n % 5 == 0:
            print("buzz")
        else:
            print(n)


print(' '.join([t for t in [e[1]+'buzz' if not e[0] % 5 else e[1] or str(e[0]) for e in [(s, 'fizz' if not s % 3 else '') for s in range(1, 101)]]]))
