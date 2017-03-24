import os


class AOpen:
    END_OF_FILE = bytes('', encoding='utf8')
    NEW_LINE = bytes('\n', encoding='utf8')

    def __init__(self, file_name, flags, encoding='utf8'):
        self.description = os.open(file_name, self.pars_flags(flags))
        self.encoding = encoding
        self.offset = 0

    def pars_flags(self, op):
        flags = {'r': os.O_RDONLY,
                 'w': os.O_WRONLY,
                 'rw': os.O_RDWR,
                 'a': os.O_APPEND
                 }
        return flags.get(op)

    def read(self, n=-1):
        data = ''
        offset = 0
        if n <= -1:
            while os.pread(self.description, 1, offset):
                data += str(os.pread(self.description, 1, offset), self.encoding)
                offset += 1
        else:
            while offset != n:
                data += str(os.pread(self.description, 1, offset), self.encoding)
                offset += 1

        return data

    def readLine(self):
        data = ''
        while os.pread(self.description, 1, self.offset) not in [self.NEW_LINE, self.END_OF_FILE]:
            data += str(os.pread(self.description, 1, self.offset), self.encoding)
            self.offset += 1
        self.offset += 1
        return data

    def write(self, data):
        os.write(self.description, bytes(data, self.encoding))

    def writeLine(self, data):
        os.write(self.description, bytes('\n' + data, self.encoding))

    def close(self):
        os.close(self.description)


f = AOpen('test.txt', 'rw')

f.write("Test Text")
f.write("Test")

f.writeLine("test test")

text = f.readLine()
print(text)
text = f.readLine()
print(text)
text = f.readLine()
print(text)

f.close()

print(text)
