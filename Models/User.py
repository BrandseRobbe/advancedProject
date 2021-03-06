import hashlib
import os
import re


class User:
    def __init__(self, name, nickname, email, password):
        self.name = name
        self.nickname = nickname
        self.email = email
        self.password = password

    @staticmethod
    def isValidEmail(email):
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if re.search(regex, email):
            return True
        else:
            return False
    @staticmethod
    def isValidPassword(password):
        pat = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%_*#?&])[A-Za-z\d@$!#%_*?&]{6,20}$")
        if re.search(pat, password):
            return True
        else:
            return False
    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        if self.isValidPassword(password):
            self.__password = hashlib.sha256(password.encode()).hexdigest()
        else:
            raise ValueError
    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        if self.isValidEmail(email):
            self.__email = email
        else:
            raise ValueError
