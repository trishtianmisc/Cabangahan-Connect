import psycopg2

class Database:
    def __init__(self):
        self.__conn = None
        self.__cursor = None
        self.__dbname = "Cabangahan"
        self.__user = "postgres"
        self.__password = "1234"
        self.__host = "localhost"
        self.__port = "5432"

    def set_connection(self):
        if self.__conn is None:
            try:
                self.__conn = psycopg2.connect(
                    dbname = self.__dbname,
                    user = self.__user,
                    password = self.__password,
                    host = self.__host,
                    port = self.__port
                )
                self.__cursor = self.__conn.cursor()
            except psycopg2.Error as e:
                print(f"Database connection error: {e}")

    def get_connection(self):
        return self.__conn

    def get_cursor(self):
        return self.__cursor

    def close_connection(self):
        try:
            if self.__cursor:
                self.__cursor.close()
                self.__cursor = None
            if self.__conn:
                self.__conn.close()
                self.__conn = None
        except Exception as e:
            print(f"Error closing connection: {e}")