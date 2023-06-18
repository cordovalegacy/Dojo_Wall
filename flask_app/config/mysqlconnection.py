import pymysql.cursors
# a cursor is the object we use to interact with the database


class MySQLConnection:
    # this class will give us an instance of a connection to our database
    def __init__(self, db):
        # change the user and password configurations as needed
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            db=db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        self.connection = connection
        # line 18 establishes the connection to the database

    def query_db(self, query, data=None):
        # this function/method will query the database
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)

                cursor.execute(query, data)
                if query.lower().find('insert') >= 0:
                    self.connection.commit()
                    # INSERT queries will return the ID NUMBER of the row inserted
                    return cursor.lastrowid
                elif query.lower().find('select') >= 0:
                    # SELECT queries will return the data from the database as a LIST of DICTIONARIES
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
                    # UPDATE and DELETE queries will return nothing
            except Exception as e:
                print("Something went wrong", e)
                return False
                # if the query fails the function/method will return false
            finally:
                self.connection.close()
                # closes the connection


def connectToMySQL(db):
    # connectToMySQL receives the database we're using and uses it to create an instance of MySQLConnection
    return MySQLConnection(db)
