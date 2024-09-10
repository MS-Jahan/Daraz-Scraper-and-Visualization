import sqlite3
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import traceback
from pprint import pprint

class Database:
    def __init__(self, host, user, password, database, TRUNCATE_TABLE_BEFORE_INSERT=True):
        """Initialize the database connection and create the products table if it doesn't exist."""
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if self.conn.is_connected():
                self.cur = self.conn.cursor()
                self._create_table(TRUNCATE_TABLE_BEFORE_INSERT)
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.conn = None

    def _create_table(self, TRUNCATE_TABLE_BEFORE_INSERT):
        """Create the products table if it does not already exist."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            image TEXT,
            item_id VARCHAR(100),
            discount_percentage FLOAT,
            rating FLOAT,
            number_of_reviews INT,
            location VARCHAR(100),
            current_price FLOAT,
            original_price FLOAT,
            url TEXT,
            scrapped_at DATETIME
        )
        """
        self.cur.execute(create_table_query)
        self.conn.commit()
        if TRUNCATE_TABLE_BEFORE_INSERT:
            truncate_table_query = "TRUNCATE TABLE products"
            self.cur.execute(truncate_table_query)
            self.conn.commit()

    def query_db(self, query, args=(), one=False):
        """Execute a query and return the results as a list of dictionaries."""
        self.cur.execute(query, args)
        columns = [desc[0] for desc in self.cur.description]
        rows = [dict(zip(columns, row)) for row in self.cur.fetchall()]
        return rows[0] if rows else None if one else rows

    def get_all_data(self):
        """Return all data from the products table."""
        query = "SELECT * FROM products"
        return self.query_db(query)

    def insert(self, product):
        """Insert a single product into the database."""
        insert_query = """
        INSERT INTO products (
            name, image, item_id, discount_percentage, rating,
            number_of_reviews, location, current_price, original_price,
            url, scrapped_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Debugging: Print the query and the parameters to be inserted
        # print("Executing query:", insert_query)
        # print("With parameters:", (
        #     product["name"], product["image"], product["item_id"],
        #     product["discount_percentage"], product["rating"],
        #     product["number_of_reviews"], product["location"],
        #     product["current_price"], product["original_price"],
        #     product["url"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # ))
        
        try:
            self.cur.execute(insert_query, (
                product["name"], product["image"], product["item_id"],
                product["discount_percentage"], product["rating"],
                product["number_of_reviews"], product["location"],
                product["current_price"], product["original_price"],
                product["url"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            self.conn.commit()
            # Return the row ID of the last inserted row
            return self.cur.lastrowid
        except Exception as e:
            print(f"Error inserting data: {e}")
            print(traceback.format_exc())
            return None



    def batch_insert(self, products):
        """Insert multiple products into the database in batches. Ignore if the item_id already exists."""
        if not products:
            return
        
        insert_query = """
        INSERT INTO products (
            name, image, item_id, discount_percentage, rating,
            number_of_reviews, location, current_price, original_price,
            url, scrapped_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        total_inserted = 0
        # Insert in batches
        INSERT_BATCH_SIZE = 10
        for i in range(0, len(products), INSERT_BATCH_SIZE):
            batch = products[i:i+INSERT_BATCH_SIZE]
            self.cur.executemany(insert_query, [
                (
                    product["name"], product["image"], product["item_id"],
                    product["discount_percentage"], product["rating"],
                    product["number_of_reviews"], product["location"],
                    product["current_price"], product["original_price"],
                    product["url"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ) for product in batch
            ])
            total_inserted += self.cur.rowcount  # Count how many rows were inserted
            # print(f"Inserted {total_inserted} rows...")

        self.conn.commit()
        return len(products), total_inserted  # Return the total number of products and the total inserted
    
    # def batch_insert(self, products):
    #     total_inserted = 0
    #     for index, product in enumerate(products):
    #         print(f"Inserting product {index+1}/{len(products)}...")
    #         # pprint(product)
    #         self.insert(product)
    #         print(self.cur.lastrowid)
    #         total_inserted += self.cur.rowcount
    #     self.conn.commit()
        
    #     return len(products), total_inserted

    def check_duplicate_entries_in_db(self):
        """Return a list of duplicate entries one time based on item_id."""
        query = """
        SELECT item_id, COUNT(*) AS count
        FROM products
        GROUP BY item_id
        HAVING count > 1
        """
        return self.query_db(query)



    def remove_duplicates(self):
        """Remove duplicate entries using item_id from the database, keeping the earliest entry."""
        query = """
        DELETE p1
        FROM products p1
        JOIN products p2
        WHERE p1.id > p2.id
        AND p1.item_id = p2.item_id
        """
        self.cur.execute(query)
        self.conn.commit()


    def get_total_items(self):
        """Return the total number of items in the database."""
        query = "SELECT COUNT(*) FROM products"
        return self.query_db(query, one=True)["COUNT(*)"]

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()

    def __del__(self):
        """Ensure the database connection is closed when the object is deleted."""
        self.close()

if __name__ == "__main__":
    import json
    # read all_data.json
    with open("all_data.json", "r") as f:
        all_data = json.load(f)
    
    # create a database object
    DB = Database("localhost", "root", "1234", "products")

    # insert all data to the database
    print("Inserting all data to the database...")
    proudcts_inputted, total_inserted = DB.batch_insert(all_data)
    print(f"Iems processed: {proudcts_inputted}\nItems inserted: {total_inserted}")

    # check how many duplicates are there in the data using item_id
    duplicates = DB.check_duplicate_entries_in_db()
    print(f"Total duplicate entries: {len(duplicates)}")

    pprint(duplicates)

    print(f"Total items before processed: {DB.get_total_items()}")

    if len(duplicates) > 0:
        # save duplicates to a file
        with open("duplicates.json", "w") as f:
            f.write(json.dumps(duplicates, indent=4))
        print("Removing duplicates...")
        DB.remove_duplicates()

    print(f"Total items processed: {DB.get_total_items()}")
    DB.close()
    

