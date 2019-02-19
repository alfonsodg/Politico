# imports
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class UserModel:
    """
    The v2 user model.
    """

    def __init__(self, username, email, password,
                 firstname, lastname, phone, passportUrl, isPolitician, othername, isAdmin):
        """
            Constructor of the user class
            New user objects are created with this method
        """
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.phone = phone
        self.password = self.encrypt_password_on_signup(password)
        self.passportUrl = passportUrl
        self.isPolitician = isPolitician
        self.othername = othername
        self.isAdmin = isAdmin

    def save_user(self):
        """
        Add a new user to the users table
        """
        save_user_query = """
        INSERT INTO users(username,
        firstname, lastname, phone, email,
        password, passportUrl, isPolitician, othername, isAdmin) VALUES(
            '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'
        )""".format(self.username, self.firstname, self.lastname,
                    self.phone, self.email, self.password,
                    self.passportUrl, self.isPolitician,
                    self.othername, self.isAdmin)

        db.queryData(save_user_query)

    @staticmethod
    def get_user(mechanism="email", value=""):
        """
            this method helps in reusing whether we want
            to check the user by ID or by email or username.
        """
        select_user_by_email = """
        SELECT id, username, password, email FROM users
        WHERE users.{} = '{}'""".format(mechanism, value)

        return db.select_data_from_db(select_user_by_email)

    def encrypt_password_on_signup(self, password):
        """
            hash password on sign up
        """
        hashed_password = generate_password_hash(str(password))
        return hashed_password

    @staticmethod
    def get_user_by_mail(email):
        return UserModel.get_user(mechanism="email", value=email)

    @staticmethod
    def get_user_by_id(id):
        """
            retrieve a user based on the ID.
            provided in the arguments.
        """
        return UserModel.get_user(mechanism="id", value=id)

    @staticmethod
    def get_user_by_id_formatted(id):
        """
            returns a record of a user
        """
        data = UserModel.get_user_by_id(id)
        d = {
            "id": data[0][0],
            "username": data[0][1],
            "email": data[0][3]
        }

        return d

    @staticmethod
    def check_if_password_n_hash_match(password_hash, password):
        return check_password_hash(password_hash, str(password))
