import json
import os
class User:
    def __init__(self, username, password, user_id, role):
        self._username = username
        self._password = password
        self.user_id = user_id
        self.role = role

    def check_password(self, password):
        return self._password == password

    def get_username(self):
        return self._username


class Admin(User):
    def __init__(self, username, password, user_id):
        super().__init__(username, password, user_id, "Admin")


class Manager(User):
    def __init__(self, username, password, user_id):
        super().__init__(username, password, user_id, "Manager")


class Employee(User):
    def __init__(self, username, password, user_id):
        super().__init__(username, password, user_id, "Employee")


class AuthManager:
    def __init__(self):
        self.users = {}

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.json_file_path = os.path.join(base_dir, "users.json")

        self.load_users_from_json()

    def load_users_from_json(self):
        try:
            with open(self.json_file_path, "r") as file:
                users_data = json.load(file)

                for u in users_data:
                    role = u.get("role")
                    username = u.get("username")
                    password = u.get("password")
                    user_id = u.get("user_id")

                    if role == "Admin":
                        user_obj = Admin(username, password, user_id)
                    elif role == "Manager":
                        user_obj = Manager(username, password, user_id)
                    elif role == "Employee":
                        user_obj = Employee(username, password, user_id)
                    else:
                        user_obj = User(username, password, user_id, role)

                    self.users[username] = user_obj
        except FileNotFoundError:
            print(f"⚠️ Warning: File '{self.json_file_path}' not found.")
        except json.JSONDecodeError:
            print(f"⚠️ Error: Invalid JSON format in '{self.json_file_path}'.")

    def save_users_to_json(self):
        users_data = []

        for user in self.users.values():
            users_data.append({
                "username": user.get_username(),
                "password": user._password,
                "user_id": user.user_id,
                "role": user.role
            })

        with open(self.json_file_path, "w") as file:
            json.dump(users_data, file, indent=4)

    def add_user(self, username, password, role):
        role = role.strip().capitalize()

        if username in self.users:
            print("Username already exists.")
            return

        user_id = len(self.users) + 1

        if role == "Admin":
            user = Admin(username, password, user_id)

        elif role == "Manager":
            user = Manager(username, password, user_id)

        elif role == "Employee":
            user = Employee(username, password, user_id)

        else:
            print("Invalid role.")
            return

        self.users[username] = user

        self.save_users_to_json()

        print("User added successfully.")


    def register_user(self, user):
        self.users[user.get_username()] = user

    def login(self, username, password):

        print("Searching for:", repr(username))

        user = self.users.get(username)

        print("User Found:", user)

        if user:
            print("Stored Password:", repr(user._password))
            print("Entered Password:", repr(password))
            print("Password Match:", user.check_password(password))

        if user and user.check_password(password):
            print("Login Success")
            return user

        print("Login Failed")
        return None

