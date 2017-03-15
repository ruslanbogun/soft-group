def like(numbers: str, a_set: str, b_set: str):
    return sum(map(lambda c: 1 if c[0] == True else -1, filter(lambda t: t[0] != t[1], [(s in a_set.split(" "), s in b_set.split(" ")) for s in numbers.split(" ")])))

numbers = '3 2 10 7 5 5 2 1 2'
a = '2 3 7'
b = '5 10 7'
print(like(numbers, a, b))

numbers = '1 4 10 20 1 11 12'
a = '1 4 1 12'
b = '1 12 10 20'
print(like(numbers, a, b))
