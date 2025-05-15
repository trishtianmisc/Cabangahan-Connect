import psycopg2
import psycopg2.extras
from ResidentList import ResidentList

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.dbname = "BarangayCabangahan"
        self.user = "postgres"
        self.password = "1234"
        self.host = "localhost"
        self.port = "5432"

    def set_connection(self):
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    dbname=self.dbname,
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port
                )
                # Use DictCursor to access results by column name
                self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            except psycopg2.Error as e:
                print(f"[Database Error] Connection failed: {e}")
                self.conn = None
                self.cursor = None

    def get_connection(self):
        return self.conn

    def get_cursor(self):
        return self.cursor

    def commit(self):
        if self.conn:
            self.conn.commit()

    def rollback(self):
        if self.conn:
            self.conn.rollback()

    def close_connection(self):
        try:
            if self.cursor:
                self.cursor.close()
                self.cursor = None
            if self.conn:
                self.conn.close()
                self.conn = None
        except Exception as e:
            print(f"[Database Error] Failed to close connection: {e}")

    def fetch_residents(self):
        self.set_connection()  # Ensure connection is set before using it

        if self.cursor is None:
            print("[Error] Cursor not initialized.")
            return []

        try:
            self.cursor.execute("""
                SELECT RES_FIRSTNAME, RES_LASTNAME, RES_MIDDLENAME, RES_DATEOFBIRTH,
                    RES_PLACEOFBIRTH, RES_NATIONALITY, RES_RELIGION, RES_PUROK,
                    RES_GENDER, RES_PWD, RES_DECEASED, RES_BLOODTYPE, RES_HEIGHT,
                    RES_FATHER, RES_MOTHER
                FROM RESIDENT
            """)
            rows = self.cursor.fetchall()
            return [ResidentList(*row) for row in rows]
        except Exception as e:
            print(f"[Database Error] Failed to fetch residents: {e}")
            return []
        finally:
            self.close_connection()

