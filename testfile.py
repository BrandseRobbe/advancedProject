from Models.User import User
from Models.PickleRepo import PickleRepo

user = User("qsldkfjqsmdlkfjsqldkmjf", "azerty")
pickle = PickleRepo()
# print(pickle.readFile())
pickle.updfateFile(user)
# pickle.overWriteFile([user])
data = pickle.readFile()
# data.append(user)
print(data[1].username)
