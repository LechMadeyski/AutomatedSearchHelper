class UserDatabase:
    def __init__(self):
        self._users = {'admin': {'password': 'admin', 'display_name': 'Admin'}}

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
            return True, "Successfully created user"

    def get_full_name(self, login):
        user = self._users.get(login)
        if user:
            return user['display_name']
        else:
            return 'Unknown'


user_database = UserDatabase()


def get_user_database():
    global user_database
    return user_database
