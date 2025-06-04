from PyQt5.QtCore import QThread, pyqtSignal
import psycopg2
import select

class DBListener(QThread):
    notify_signal = pyqtSignal()

    def run(self):
        conn = psycopg2.connect("dbname=BarangayCabangahan user=postgres password=1234")
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("LISTEN resident_update;")
        print("Listening for resident updates...")

        while True:
            if select.select([conn], [], [], 5) == ([], [], []):
                continue
            conn.poll()
            while conn.notifies:
                notify = conn.notifies.pop(0)
                print("Resident notification:", notify.payload)
                self.notify_signal.emit()
