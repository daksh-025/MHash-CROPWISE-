import psycopg2

class TransactionFetcher:
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

    def fetch_transactions_by_user(self, userfinal, passfinal):
        query = "SELECT * FROM farmersindian WHERE username = %s AND password = %s;"


        with self.conn.cursor() as cursor:
            cursor.execute(query, (userfinal, passfinal))
            result = cursor.fetchone()
            print(result)
            
            if result:
                transactions = result
                return transactions
            else:
                return None

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

    def process_request(self, customer_id, first_name, last_name):
        

        transactions = self.fetch_transactions_by_user(customer_id, first_name, last_name)

        if transactions:
            print(f"Transactions for {first_name} {last_name}:")
            #for transaction in transactions:
                #print(transaction)
            return 1
        else:
            print("User does not exist.")
            return 0

    def __del__(self):
        self.close_connection()  # Close the database connection when the instance is deleted

if __name__ == "__main__":
    db_params = {
        'dbname': 'Converge',
        'user': 'postgres',
        'password': 'justdoit03#',
        'host': 'localhost'
    }
    customer_id = int(input("Enter customer_id: "))
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    transaction_fetcher = TransactionFetcher(db_params)
    transaction_fetcher.process_request(customer_id, first_name, last_name)
