import json

import jsonpickle

from Models.User import User


user0 = User("name", "nickname", "test@mail.il",  "Azerty_8")
user1 = User("name", "nickname", "test@mail.il",  "Azerty_8")
user2 = User("name", "nickname", "test@mail.il",  "Azerty_8")
print(user0.password)
print(user2.password)
print(user1.password)

# gepickled = jsonpickle.encode(user)
# testdict = {"type": "test", "value": gepickled}
# testdict = json.dumps(testdict)
# print(testdict)
#
#
# jsonobject = json.loads(testdict)
# print(type(jsonobject))
# pickle = jsonobject["value"]
# print(type(pickle))
# ontpickled = jsonpickle.decode(pickle)
# print(ontpickled.email)




# pickle = PickleRepo()
# # print(pickle.readFile())
# pickle.updfateFile(user)
# # pickle.overWriteFile([user])
# data = pickle.readFile()
# # data.append(user)
# print(data[1].username)
