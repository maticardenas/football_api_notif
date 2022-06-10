from src.db.db_manager import NotifierDBManager
from src.db.notif_sql_models import *

if __name__ == "__main__":
    notifier_db_manager = NotifierDBManager()
    notifier_db_manager.create_db_and_tables()