from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash, session


class Post:
    db = "dojo_wall"

    def __init__(self, post):
        self.id = post['id']
        self.user_id = post['user_id']
        self.content = post['title']
        self.created_at = post['created_at']
        self.updated_at = post['updated_at']
        self.posted_by = []  # one to many cls assoc.
        self.comments = []  # many to many cls assoc.

# !Helper Methods
    def __str__(self):
        # Return a string representation of the object
        return f"Post ID: {self.id}, Content: {self.content}, Posted By: {self.posted_by}, Comments: {self.comments}"

    def comment(self, id):
        found_user = None
        for user in self.comments:
            if user.id == id:
                found_user = user
        return found_user != None

# !Create

    # *create a new show in the db
    @classmethod
    def save_posts(cls, data):
        query = """
                INSERT INTO posts (content, user_id)
                VALUES (%(content)s, %(user_id)s)
                ;"""
        return connectToMySQL(cls.db).query_db(query, data)

    # *create a new like in the joining table (uses both shows and users)
    @classmethod
    def like_show(cls, data):
        query = """
                INSERT INTO users_shows
                (show_id, user_id)
                VALUES
                (%(show_id)s, %(user_id)s)
                """
        return connectToMySQL(cls.db).query_db(query, data)


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
        results = connectToMySQL(cls.db).query_db(query, data)
        result = cls(results[0])
        print(result)
        likes_query = """
                        SELECT COUNT(*) as total_likes FROM users_shows
                        WHERE show_id = %(id)s;
                        """
        likes_results = connectToMySQL(cls.db).query_db(likes_query, data)
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

    # *from Robert Ponce (many to many) gets all posts for post table
    @classmethod
    def get_all_posts_with_user(cls):
        query = """
                SELECT * FROM posts
                LEFT JOIN users 
                ON posts.user_id = users.id
                LEFT JOIN comments
                ON posts.id = comments.post_id
                LEFT JOIN users AS poster
                ON comments.user_id = poster.id
                ;"""
        results = connectToMySQL(cls.db).query_db(query)
        if not results:
            return []
        posts = []
        this_post = None
        for row in results:
            if this_post == None or this_post.id != row['id']:
                this_post = cls(row)
                data = {
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': "",
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                this_post.posted_by = user.User(data)
                posts.append(this_post)

            if not row['comments.user_id'] == None:
                data = {
                    'id': row['poster.id'],
                    'first_name': row['poster.first_name'],
                    'last_name': row['poster.last_name'],
                    'email': row['poster.email'],
                    'password': "",
                    'created_at': row['poster.created_at'],
                    'updated_at': row['poster.updated_at']
                }
                this_post.comments.append(user.User(data))
        print(posts[0])
        return posts

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
        return connectToMySQL(cls.db).query_db(query, data)

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
        return connectToMySQL(cls.db).query_db(query, data)

    # *delete a show from the db
    @classmethod
    def delete_show(cls, data):
        query = """
                DELETE FROM shows 
                WHERE shows.id = %(id)s
                ;"""
        return connectToMySQL(cls.db).query_db(query, data)

# !Validations

    # *handles post creation validation
    @staticmethod
    def validate_post(form_data):
        is_valid = True
        if not form_data['content']:
            flash("Content of post must not be left blank", 'Posts')
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
    #     results = connectToMySQL(cls.db).query_db(query, data)
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
