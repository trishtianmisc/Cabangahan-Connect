# auth.py


from DATABASE.database import Database
class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.db = Database()
        self.db.set_connection()
        self.cursor = self.db.get_cursor()

    def is_valid(self):
        try:
            query = "SELECT * FROM ACCOUNT WHERE USERNAME = %s AND PASS = %s"
            self.cursor.execute(query, (self.username, self.password))
            result = self.cursor.fetchone()

            if result:
                return True
            else:
                return False

        except Exception as e:
          print(f"Login check failed: {e}")
          return False


    def close(self):
       self.db.close_connection()
