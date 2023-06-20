from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash


class Post:
    db = "dojo_wall"

    def __init__(self, post):
        self.id = post['id']
        self.user_id = post['user_id']
        self.content = post['content']
        self.created_at = post['created_at']
        self.updated_at = post['updated_at']
        self.posted_by = None  # one to many cls assoc.
        self.comments = []  # many to many cls assoc.

# !Helper Methods
    def __str__(self):
        # Return a string representation of the object
        comments_str = ', '.join(str(comment) for comment in self.comments)
        return f"Post ID: {self.id}, Content: {self.content}, Posted By: {self.posted_by}, Comments: {comments_str}"

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
    def create_comment(cls, data):
        query = """
                INSERT INTO comments
                (post_id, comment, user_id)
                VALUES
                (%(post_id)s, %(comment)s, %(user_id)s)
                """
        return connectToMySQL(cls.db).query_db(query, data)


# !Render

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
                comment_data = {
                    'id': row['poster.id'],
                    'first_name': row['poster.first_name'],
                    'last_name': row['poster.last_name'],
                    'email': row['poster.email'],
                    'password': "",
                    'created_at': row['poster.created_at'],
                    'updated_at': row['poster.updated_at'],
                    'comment': row['comment'],
                }
                this_post.comments.append(comment_data)
        print("all posts---->", posts)
        return posts

# !Update


# !Delete

    # *delete a show from the db
    @classmethod
    def delete_post(cls, data):
        query = """
                DELETE FROM posts 
                WHERE posts.id = %(id)s
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