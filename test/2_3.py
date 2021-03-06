# coding=utf-8
# Дана функция adder. На вход она получает произвольное количество
# целочисленных неименованных аргументов. На выход возвращает сумму
# квадратов всех переданных аргументов. Допишите пропущенные участки
# кода функции.

def adder(*l):
    return sum(map(lambda x: x * x, l))

# Test
print(adder(1, 2, 3, 4, 5))

print(adder(55, 13, 10, 20))
