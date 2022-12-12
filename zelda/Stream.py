class stream:

    def __init__(self, data):
        self.data = data

    def string(self):
        strings = []
        while True:
            read = self.data.readline()
            if read[5:10] == '━━━━━':
                return ''.join(strings)
            strings.append(read)

    def readline(self):
        return self.data.readline()

    def seek(self, offset, origin=0):
        return self.data.seek(offset, origin)

    def tell(self):
        return self.data.tell()

    def read(self, read=-1):
        return self.data.read(read)

    def write(self, data):
        return self.data.write(data)

    def close(self):
        return self.data.close()
