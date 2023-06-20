from flask_app.config.mysqlconnection import connectToMySQL

class Comment:
    db = "dojo_wall"

    def __init__(self, comment):
        self.user_id = comment['user_id']
        self.post_id = comment['post_id']
        self.comment = comment['comment']

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