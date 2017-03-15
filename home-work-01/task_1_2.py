def fine_print(n: int):
    s = list(map(lambda x: "".join(x), [list(map(lambda e: e.ljust(10, " "), (str(n), oct(n)[2:], hex(n)[2:].upper(), bin(n)[2:]))) for n in range(1, n + 1)]))
    print("\n".join(p for p in s))


fine_print(13)
