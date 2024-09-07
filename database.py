import sqlite3
from datetime import datetime
import traceback

class Database:
    def __init__(self, db):
        """Initialize the database connection and create the products table if it doesn't exist."""
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """Create the products table if it does not already exist."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            image TEXT,
            item_id TEXT UNIQUE,
            discount_percentage FLOAT,
            rating FLOAT,
            number_of_reviews FLOAT,
            location TEXT,
            current_price FLOAT,
            original_price FLOAT,
            url TEXT,
            created_at DATETIME
        )
        """
        self.cur.execute(create_table_query)
        self.conn.commit()

    def query_db(self, query, args=(), one=False):
        """Execute a query and return the results as a list of dictionaries."""
        self.cur.execute(query, args)
        columns = [desc[0] for desc in self.cur.description]
        rows = [dict(zip(columns, row)) for row in self.cur.fetchall()]
        return rows[0] if rows else None if one else rows

    def insert(self, product):
        """Insert a single product into the database."""
        insert_query = """
        INSERT INTO products (
            name, image, item_id, discount_percentage, rating,
            number_of_reviews, location, current_price, original_price,
            url, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.cur.execute(insert_query, (
            product["name"], product["image"], product["item_id"],
            product["discount_percentage"], product["rating"],
            product["number_of_reviews"], product["location"],
            product["current_price"], product["original_price"],
            product["url"], datetime.now()
        ))
        self.conn.commit()

    def batch_insert(self, products):
        """Insert multiple products into the database in batches."""
        if not products:
            return
        
        insert_query = """
        INSERT INTO products (
            name, image, item_id, discount_percentage, rating,
            number_of_reviews, location, current_price, original_price,
            url, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        # Insert in batches of 10
        for i in range(0, len(products), 10):
            batch = products[i:i+10]
            self.cur.executemany(insert_query, [
                (
                    product["name"], product["image"], product["item_id"],
                    product["discount_percentage"], product["rating"],
                    product["number_of_reviews"], product["location"],
                    product["current_price"], product["original_price"],
                    product["url"], datetime.now()
                ) for product in batch
            ])
        self.conn.commit()

    def check_duplicate_entries_in_db(self):
        """Return a list of duplicate entries based on item_id."""
        query = """
        SELECT item_id, name, COUNT(*)
        FROM products
        GROUP BY item_id
        HAVING COUNT(*) > 1
        """
        return self.query_db(query)

    def remove_duplicates(self):
        """Remove duplicate entries from the database, keeping the earliest entry."""
        query = """
        DELETE FROM products
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM products
            GROUP BY item_id
        )
        """
        self.cur.execute(query)
        self.conn.commit()

    def get_total_items(self):
        """Return the total number of items in the database."""
        query = "SELECT COUNT(*) FROM products"
        return self.query_db(query, one=True)

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()

    def __del__(self):
        """Ensure the database connection is closed when the object is deleted."""
        self.close()
