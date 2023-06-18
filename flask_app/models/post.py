from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash, session


class Show:

    def __init__(self, show):
        self.id = show['id']
        self.title = show['title']
        self.network = show['network']
        self.release_date = show['release_date']
        self.description = show['description']
        self.created_at = show['created_at']
        self.updated_at = show['updated_at']
        self.viewers = [] #one to many cls assoc.
        self.likes = [] #many to many cls assoc.

# !Helper Methods
    def __str__(self):
        # Return a string representation of the object
        # likes_str = ', '.join(str(user) for user in self.likes)
        return f"Show ID: {self.id}, Title: {self.title}, Viewers: {self.viewers}, Likes: {self.likes}"

    def liked_by(self, id):
        found_user = None
        for user in self.likes:
            if user.id == id:
                found_user = user
        return found_user != None

# !Create

    # *create a new show in the db
    @classmethod
    def save_shows(cls, data):
        query = """
                INSERT INTO shows (title, network, release_date, description, user_id)
                VALUES (%(title)s, %(network)s, %(release_date)s, %(description)s, %(user_id)s)
                ;"""
        return connectToMySQL('tv_shows').query_db(query, data)

    # *create a new like in the joining table (uses both shows and users)
    @classmethod
    def like_show(cls, data):
        query = """
                INSERT INTO users_shows
                (show_id, user_id)
                VALUES
                (%(show_id)s, %(user_id)s)
                """
        return connectToMySQL('tv_shows').query_db(query, data)


# !Render

    # *render a single show's data connected to a user

    @classmethod
    def display_single_show(cls, data):
        query = """
                SELECT * FROM shows
                LEFT JOIN users ON shows.user_id = users.id
                LEFT JOIN users_shows ON shows.id = users_shows.show_id
                WHERE shows.id = %(id)s
                ;"""
        results = connectToMySQL('tv_shows').query_db(query, data)
        result = cls(results[0])
        print(result)
        likes_query = """
                        SELECT COUNT(*) as total_likes FROM users_shows
                        WHERE show_id = %(id)s;
                        """
        likes_results = connectToMySQL('tv_shows').query_db(likes_query, data)
        print("likes results", likes_results)
        result.likes = likes_results[0]['total_likes']
        for row in results:
            if row['users.id'] == None:
                break
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': "",
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            result.viewers.append(user.User(user_data))
        print("Appended Result", result)
        return result

    # *from Robert Ponce (many to many) gets all shows for shows table
    @classmethod
    def get_all_shows_with_user(cls):
        query = """
                SELECT * FROM shows
                LEFT JOIN users 
                ON shows.user_id = users.id
                LEFT JOIN users_shows
                ON shows.id = users_shows.show_id
                LEFT JOIN users AS liked_by
                ON users_shows.user_id = liked_by.id
                ;"""
        results = connectToMySQL('tv_shows').query_db(query)
        if not results:
            return []
        shows = []
        this_show = None
        for row in results:
            if this_show == None or this_show.id != row['id']:
                this_show = cls(row)
                data = {
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': "",
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                this_show.viewers = user.User(data)
                shows.append(this_show)

            if not row['users_shows.user_id'] == None:
                data = {
                    'id': row['liked_by.id'],
                    'first_name': row['liked_by.first_name'],
                    'last_name': row['liked_by.last_name'],
                    'email': row['liked_by.email'],
                    'password': "",
                    'created_at': row['liked_by.created_at'],
                    'updated_at': row['liked_by.updated_at']
                }
                this_show.likes.append(user.User(data))
        print(shows[0])
        return shows

# !Update

    # *update the show in the db
    @classmethod
    def edit_show(cls, data):
        query = """
                UPDATE shows 
                SET 
                title = %(title)s, 
                network = %(network)s, 
                release_date = %(release_date)s, 
                description = %(description)s, 
                updated_at = NOW() 
                WHERE id=%(id)s
                ;"""
        return connectToMySQL('tv_shows').query_db(query, data)

# !Delete

    # *delete a like in the db from joining table
    @classmethod
    def dislike_show(cls, data):
        query = """
                DELETE FROM users_shows
                WHERE
                show_id=%(show_id)s
                AND
                user_id=%(user_id)s
                """
        return connectToMySQL('tv_shows').query_db(query, data)

    # *delete a show from the db
    @classmethod
    def delete_show(cls, data):
        query = """
                DELETE FROM shows 
                WHERE shows.id = %(id)s
                ;"""
        return connectToMySQL('tv_shows').query_db(query, data)

# !Validations

    # *handles show creation validation
    @staticmethod
    def validate_show(form_data):
        is_valid = True
        if not form_data['title']:
            flash("Title of show must not be left blank", 'Shows')
            is_valid = False
        if not form_data['network']:
            flash("Network must not be left blank", 'Shows')
            is_valid = False
        if not form_data['release_date']:
            flash("Release date must not be left blank", 'Shows')
            is_valid = False
        if len(form_data['description']) < 3:
            flash("Description must be at least 3 characters", 'Shows')
            is_valid = False
        return is_valid


# !Unused but may need
    # *shows liked shows (did not use... but part of Robert Ponce Many to Many Lecture)
    # @classmethod
    # def users_like_shows(cls, data):
    #     query = """
    #             SELECT * FROM shows
    #             LEFT JOIN users
    #             ON shows.user_id = users.id
    #             LEFT JOIN users_shows
    #             ON shows.id = users_shows.show_id
    #             LEFT JOIN users AS liked_by
    #             ON users_shows.user_id = liked_by.id
    #             WHERE shows.id = %(show_id)s
    #             """
    #     results = connectToMySQL('tv_shows').query_db(query, data)
    #     this_show = cls(results[0])
    #     data = {
    #         'id': results[0]['users.id'],
    #         'first_name': results[0]['first_name'],
    #         'last_name': results[0]['last_name'],
    #         'email': results[0]['email'],
    #         'password': results[0]['password'],
    #         'created_at': results[0]['users.created_at'],
    #         'updated_at': results[0]['users.updated_at']
    #     }
    #     this_viewer = user.User(data)
    #     this_show.viewers = this_viewer
    #     for row in results:
    #         if not row['users_shows.user_id'] == None:
    #             data = {
    #                 'id': row['liked_by.id'],
    #                 'first_name': row['liked_by.first_name'],
    #                 'last_name': row['liked_by.last_name'],
    #                 'email': row['liked_by.email'],
    #                 'password': "",
    #                 'created_at': row['liked_by.created_at'],
    #                 'updated_at': row['liked_by.updated_at']
    #             }
    #             this_show.likes.append(user.User(data))
    #     print("--->", this_show.id)
    #     return this_show
