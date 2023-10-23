import psycopg2

import psycopg2

class InventoryFetcher:
    def __init__(self, db_params):
        self.db_params = db_params
        self.conn = None
        self.connect()  # Establish the database connection in the constructor

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.db_params)
            print("Connected to the database.")
        except psycopg2.Error as e:
            print("Error:", e)
    def fetch_stock(self):
        query2 = "SELECT * FROM inventory;"
        with self.conn.cursor() as cursor2:
            cursor2.execute(query2, ())
            results = cursor2.fetchall()
            if results:
                stock_list = [(item_name, stock_remaining) for item_name, stock_remaining in results]
                return stock_list
            else:
                return []

    def fetch_stock_by_item(self, item_name):
        query = "SELECT stock_remaining FROM inventory WHERE item_name = %s;"
        with self.conn.cursor() as cursor:
            cursor.execute(query, (item_name,))
            result = cursor.fetchone()
            if result:
                stock_remaining = result[0]
                return stock_remaining
            else:
                return None

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

    def process_request(self):
        item_name = input("Enter item name: ")

        stock_remaining = self.fetch_stock_by_item(item_name)

        if stock_remaining is not None:
            print(f"Stock remaining for {item_name}: {stock_remaining}")
        else:
            print("Item not found in inventory.")

    def __del__(self):
        self.close_connection()  # Close the database connection when the instance is deleted

if __name__ == "__main__":
    db_params = {
        'dbname': 'Converge2',
        'user': 'postgres',
        'password': 'justdoit03#',
        'host': 'localhost'
    }

    inventory_fetcher = InventoryFetcher(db_params)
    inventory_fetcher.process_request()
