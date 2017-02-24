# coding=utf-8
# Дана функция, принимающая на входе число введенное пользователем и
# возвращающая True в случае, если число четное, и False в случае ввода
# нечетного число. Допишите пропущенный участок кода функции:

def func():
    number = input('Type a number: ')
    return int(number) % 2 == 0

# Test
if func():
    print('Number you typed is an even number')
else:
    print('Number you typed is an odd number')
