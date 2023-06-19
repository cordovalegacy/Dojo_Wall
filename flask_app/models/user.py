from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import post
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db = "dojo_wall" 
    def __init__(self, user):
        self.id = user['id']
        self.first_name = user['first_name']
        self.last_name = user['last_name']
        self.email = user['email']
        self.password = user['password']
        self.created_at = user['created_at']
        self.updated_at = user['updated_at']
        self.posts = []

# !Helper Methods

    # *Return a string representation of the object
    def __str__(self):
        return f"User ID: {self.id}, Name: {self.first_name} {self.last_name}, Email: {self.email}"

# !Create

    # *register a user
    @classmethod
    def save(cls, user_data):
        query = """
                INSERT INTO users (first_name, last_name, email, password) 
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
                ;"""
        return connectToMySQL(cls.db).query_db(query, user_data)

# !Render

    # *needed to check if email exists already during reg or login
    @classmethod
    def get_one_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email=%(email)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
    

# !Validations

    # *validate registration
    @staticmethod
    def validate(form_data):
        is_valid = True
        query = """
                SELECT * FROM users 
                WHERE email = %(email)s
                ;"""
        results = connectToMySQL("dojo_wall").query_db(query, form_data)
        if len(results) >=1:
            flash("Email is taken, enter a different one", 'Register')
            is_valid = False
        if len(form_data['first_name']) < 2:
            flash("First Name must be at least 2 characters", 'Register')
            is_valid = False
        if len(form_data['last_name']) < 2:
            flash("Last Name must be at least 2 characters", 'Register')
            is_valid = False
        if not EMAIL_REGEX.match(form_data['email']):
            flash("Please register with a valid email address", 'Register')
            is_valid = False
        if len(form_data['password']) < 7:
            flash("Password must be at least 7 characters", 'Register')
            is_valid = False
        if form_data['password'] != form_data['confirm']:
            flash("Passwords must match", 'Register')
            is_valid = False
        return is_valid
    
# !Unused but may still need
    # *render all users
    # @classmethod
    # def display_all_users(cls):
    #     query = """
    #             SELECT * FROM users
    #             ;"""
    #     results = connectToMySQL(cls.db).query_db(query)
    #     users = []
    #     for user in results:
    #         users.append(cls(user))
    #     return users

    # *got from books asgmt
    # @classmethod
    # def non_favorite_users(cls, non_favorites_data):
    #     query = """
    #             SELECT * FROM users 
    #             WHERE users.id 
    #             NOT IN
    #             (SELECT user_id FROM users_books WHERE book_id = %(id)s)
    #             ;"""
    #     results = connectToMySQL(cls.db).query_db(query, non_favorites_data)
    #     print(results)
    #     users = []
    #     for row in results:
    #         print(row)
    #         users.append(cls(row))
    #     return users

    # *shows a single user's data
    # @classmethod
    # def display_single_user(cls, single_user):
    #     query = """
    #             SELECT * FROM users 
    #             WHERE id = %(user_id)s
    #             ;"""
    #     results = connectToMySQL(cls.db).query_db(query, single_user)
    #     return cls(results[0])

    # *if we need to join a field to the users for any reason
    # @classmethod
    # def join_users_and_shows(cls, users_and_shows):
    #     query = """
    #             SELECT * FROM users 
    #             LEFT JOIN users_shows 
    #             ON users.id = users_shows.user_id
    #             LEFT JOIN shows ON shows.id = users_shows.show_id 
    #             WHERE users.id = %(user_id)s
    #             ;"""
    #     results = connectToMySQL(cls.db).query_db(query, users_and_shows)
    #     user = cls(results[0])
    #     for row in results:
    #         if row['shows.id'] == None:
    #             break
    #         shows_data = {
    #             'id': row['shows.id'],
    #             'title': row['title'],
    #             'network': row['network'],
    #             'release_date': row['release_date'],
    #             'description': row['description'],
    #             'created_at': row['shows.created_at'],
    #             'updated_at': row['shows.updated_at']
    #         }
    #         user.favorites.append(show.Show(shows_data))
    #     print(user)
    #     return user