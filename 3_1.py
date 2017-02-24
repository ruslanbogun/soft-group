# coding=utf-8
# Напишите функцию, которая на вход принимает строку, а на выход
# возвращает True, в случае если строка является палиндромом, либо
# False, если строка не палиндром. Функция не должна учитывать регистр
# букв и пробелы.

def func(a):
    w = a.upper().replace(" ", "")
    palindrome = None
    for i in range(0, int(len(w) / 2)):
        if w[i] == w[-(i + 1)]:
            palindrome = True
        else:
            palindrome = False
            break
    return palindrome

# Test
print(func('Abc b a'))  # True

print(func('xyzyq'))    # False

print(func('Eve'))      # True
