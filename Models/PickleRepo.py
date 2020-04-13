import jsonpickle


class PickleRepo:

    def __init__(self, filename="userdata.txt"):
        self.fileName = filename
        self.fileData = self.readFile()

    def readFile(self):
        my_writer_obj = open(self.fileName, mode='rb')
        json_data = my_writer_obj.read()
        data = jsonpickle.decode(json_data)
        my_writer_obj.close()
        return data

    def overWriteFile(self, object):
        my_writer_obj = open(self.fileName, mode='w')
        json_data = jsonpickle.encode(object)
        my_writer_obj.write(json_data)
        my_writer_obj.close()

    def updfateFile(self, object):
        self.fileData.append(object)
        self.overWriteFile(self.fileData)
