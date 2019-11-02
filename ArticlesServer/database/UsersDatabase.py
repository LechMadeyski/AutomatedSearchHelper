import json

from ArticlesServer.directories import USERS_FILE

class UserDatabase:
    def __init__(self):
        try:
            with open(USERS_FILE, 'r') as file_object:
                self._users = json.load(file_object)
        except FileNotFoundError:
            self._users = {'admin': {'password': 'admin', 'display_name': 'Admin'}}
            self._update_db()

    def login(self, login, password):
        user = self._users.get(login)
        if user and user['password'] == password:
            return {'login': login, 'display_name': user['display_name']}
        else:
            return None

    def register(self, login, full_name, password):
        user = self._users.get(login)
        if user:
            return False, "User already exists"
        else:
            self._users[login] = {'password': password, 'display_name': full_name}
            self._update_db()
            return True, "Successfully created user"

    def get_full_name(self, login):
        user = self._users.get(login)
        if user:
            return user['display_name']
        else:
            return 'Unknown'

    def _update_db(self):
        try:
            with open(USERS_FILE, 'w') as file_object:
                json.dump(self._users, file_object)
        except FileNotFoundError:
            print(USERS_FILE + " directory not found. could not create file ")

    def users(self):
        return self._users.keys()


user_database = UserDatabase()


def get_user_database():
    global user_database
    return user_database
