from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
import pymongo
import hashlib

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["accounts"]
mycol = mydb["customers"]



class MongoBackend:

    def register(self, requset, username=None, password=None):
        print(username, password, 'in register in pula mea ca mor de nervi')
        # mycol.insert_one({'username': username, 'pass': self.hash_password(password)})
        return User()

    def hash_password(self, password):
        return hashlib.sha256(password.encode().hexdigest()).hex()

    def authenticate(self, request, username=None, password=None):

        print(username, password)
        mycol.insert_one({'username': username, 'pass': self.hash_password(password)})
        return User()

        login_valid = (settings.ADMIN_LOGIN == username)
        pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
        if login_valid and pwd_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user. There's no need to set a password
                # because only the password from settings.py is checked.
                user = User(username=username)
                user.is_staff = True
                user.is_superuser = True
                user.save()
            return user
        return None

    def get_user(self, user_id):
        return None