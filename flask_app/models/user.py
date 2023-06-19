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