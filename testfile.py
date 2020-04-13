from Models.User import User
from Models.PickleRepo import PickleRepo

user = User("Robbe2", "azerty")
pickle = PickleRepo()
print(user.username)
pickle.writeToFile(user)

data = pickle.readFile()
print(data.username)
