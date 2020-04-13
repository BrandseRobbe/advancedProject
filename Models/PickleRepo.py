import jsonpickle


class PickleRepo:

    def __init__(self, filename="userdata.txt"):
        self.fileName = filename

    def writeToFile(self, object):
        my_writer_obj = open(self.fileName, mode='w')
        json_data = jsonpickle.encode(object)
        my_writer_obj.write(json_data)
        my_writer_obj.close()

    def readFile(self):
        my_writer_obj = open(self.fileName, mode='rb')
        json_data = my_writer_obj.read()
        data = jsonpickle.decode(json_data)
        my_writer_obj.close()
        return data