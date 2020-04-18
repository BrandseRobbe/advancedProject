import json
import re

import jsonpickle

from Models.User import User

# reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,40}$"
#
# # compiling regex
# pat = re.compile(reg)
#
# # searching regex
# mat = re.search(pat, "Azerty_8")

# pat = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%_*#?&])[A-Za-z\d@$!#%_*?&]{6,20}$")
# if re.search(pat, "Azerty_8"):
#     print("ok")
# else:
#     print("nope")


user0 = User("name", "nickname", "test@mail.il",  "Azerty_8")
# user1 = User("name", "nickname", "test@mail.il",  "Azerty_8")
# user2 = User("name", "nickname", "test@mail.il",  "Azerty_8")
# print(user0.password)
# print(user2.password)
# print(user1.password)

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
