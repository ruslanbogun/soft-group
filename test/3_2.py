# coding=utf-8
# Напишите функцию, которая в качестве аргумента принимает путь к
# каталогу с файлами. Функция должна выводить содержимое указанного
# каталога и всех вложенных подкаталогов. Желательно использовать
# рекурсию, однако подойдет любое рабочее решение.

from os import listdir
from os.path import isdir
from os.path import join as joinpath


def printDir(path):
    for f in listdir(path):
        current_path = joinpath(path, f)
        if isdir(current_path):
            print(current_path)
            printDir(current_path)
        else:
            print(current_path)

# Test
printDir("/home")
