from database import Database

def get_db(TRUNCATE_TABLE_BEFORE_INSERT):
    return Database("mysql", "root", "1234", "products", TRUNCATE_TABLE_BEFORE_INSERT)