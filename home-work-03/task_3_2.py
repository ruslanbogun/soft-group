from abc import ABC, abstractmethod
import csv
import json


def csv_load(file: object) -> str:
    data = ""
    for row in csv.reader(file, delimiter=';'):
        data += " ".join(row) + "\n"
    return data


def csv_save(s: str, file: object) -> None:
    csv_file = csv.writer(file, delimiter=';')
    for row in s.split("\n"):
        csv_file.writerow(row.split(" "))


def json_load(file: object) -> str:
    data = ""
    json_data = file.read()
    for row in json.loads(json_data)['rows']:
        data += row + "\n"
    return data


def json_save(s: str, file: object) -> None:
    json_list = list(row for row in s.split("\n"))
    file.write(json.dumps({"rows": json_list}))


class AbsConverterFabric(ABC):
    @abstractmethod
    def create_converter(self, _from: str, _to: str) -> object:
        raise NotImplemented


class AbstractConverter(ABC):
    @abstractmethod
    def load(self, file: object) -> str:
        raise NotImplemented

    @abstractmethod
    def save(self, s: str, file: object) -> object:
        raise NotImplemented


class ConverterFabric(AbsConverterFabric):
    def create_converter(self, _from: str, _to: str):
        return type("Converter", (AbstractConverter,),
                    {"load": globals()[_from + "_load"], "save": globals()[_to + "_save"]})



fab = ConverterFabric()
converter1 = fab.create_converter('csv', 'json')
converter2 = fab.create_converter('json', 'csv')

with open('csv.txt', 'r') as file:
    result = converter1.load(file)
    print(result)

with open('json.txt', 'r') as file:
    result = converter2.load(file)
    print(result)

with open('csv.txt', 'w') as file:
    converter2.save(result, file)


fab = ConverterFabric()
converter1 = fab.create_converter('csv', 'json')
converter2 = fab.create_converter('json', 'csv')

string = 'Joe Doe Green 77'

with open('json.txt', 'w') as file:
    converter1.save(string, file)

with open('json.txt', 'r') as file:
    result = converter2.load(file)

print(result)

with open('csv.txt', 'w') as file:
    converter2.save(result, file)
