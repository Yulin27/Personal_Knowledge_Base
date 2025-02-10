from src.config.settings import DATABASE
import psycopg2
import logging


logging.basicConfig(
    filename="logs/app.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class Postgres:
    """Postgres database connection class"""

    def __init__(self):
        self.conn = None
        self.cur = None

    def connect(self):
        """
        Connect to the Postgres database.
        """
        conn = psycopg2.connect(dbname=DATABASE["NAME"], user=DATABASE["USER"], password=DATABASE["PASSWORD"], host=DATABASE["HOST"], port=DATABASE["PORT"])
        cur = conn.cursor()
        self.conn = conn
        self.cur = cur
        logging.info("Connected to Postgres")

    def close(self):
        """
        Close the connection to the Postgres database.
        """
        self.cur.close()
        self.conn.close()

    def create_table(self, table_name: str, columns: dict):
        """
        Create a table in the Postgres database.
        """
        col_str = ", ".join([f"{key} {val}" for key, val in columns.items()])
        query = f"CREATE TABLE {table_name} ({col_str})"
        self.cur.execute(query)
        self.conn.commit()
        logging.info(f"Table {table_name} created")

    def insert_one_data(self, table_name: str, data: dict):
        """
        Insert data into a table in the Postgres database.
        table_name: str
        data: dict example: {"name": "John", "age": 30}
        """
        nb_keys = len(data.keys())
        query = f"INSERT INTO {table_name} ({', '.join(data.keys())}) VALUES ({', '.join(['%s']*nb_keys)})"
        self.cur.execute(query, list(data.values()))
        self.conn.commit()
        logging.info(f"Data inserted into {table_name}")

    def insert_many_data(self, table_name: str, data: list):
        """
        Insert multiple rows of data into a table in the Postgres database.
        """
        nb_keys = len(data[0].keys())
        query = f"INSERT INTO {table_name} ({', '.join(data[0].keys())}) VALUES ({', '.join(['%s']*nb_keys)})"
        data_values = [list(d.values()) for d in data]
        self.cur.executemany(query, data_values)
        self.conn.commit()
        logging.info(f"{len(data)} data inserted into {table_name}")

    def select_data(self, table_name: str, columns: list = None):
        """
        Select data from a table in the Postgres database.
        """
        if columns is None:
            columns = ["*"]
        col_str = ", ".join(columns)
        query = f"SELECT {col_str} FROM {table_name}"
        self.cur.execute(query)
        data = self.cur.fetchall()
        return data

    def delete_data(self, table_name: str, condition: str):
        """
        Delete data from a table in the Postgres database.
        """
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.cur.execute(query)
        self.conn.commit()
        logging.info(f"Data deleted from {table_name}")

    def update_data(self, table_name: str, data: dict, condition: str):
        """
        Update data in a table in the Postgres database.
        """
        set_str = ", ".join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {table_name} SET {set_str} WHERE {condition}"
        self.cur.execute(query, list(data.values()))
        self.conn.commit()
        logging.info(f"Data updated in {table_name}")

    def execute_query(self, query: str):
        """
        Execute a custom query in the Postgres database and return the result if applicable.
        """
        try:
            self.cur.execute(query)
            self.conn.commit()
            logging.info("Query executed")
            
            # Fetch results if the query produces any
            if self.cur.description:  # Check if the query returns data
                result = self.cur.fetchall()  # Fetch all rows from the result
                return result
            else:
                return None
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            self.conn.rollback()  # Roll back transaction on error
            raise


    def drop_table(self, table_name: str):
        """
        Drop a table in the Postgres database.
        """
        query = f"DROP TABLE {table_name}"
        self.cur.execute(query)
        self.conn.commit()
        logging.info(f"Table {table_name} dropped")

    def calculate_similarity(self, table_name: str):
        """
        Calculate the similarity matrix for a table in the Postgres database.
        """
        query = f"""
            SELECT a.id AS source, a.title AS source_title, a.keywords AS source_keyword, a.category AS source_category, a.summary AS source_summary,
                b.id AS target, b.title AS target_title, b.keywords AS target_keyword, b.category AS target_category, b.summary AS target_summary,
                1 - (a.embedding <=> b.embedding) AS similarity
            FROM {table_name} a, {table_name} b
            WHERE a.id != b.id
            AND 1 - (a.embedding <=> b.embedding) > 0.6
            LIMIT 100; -- Limit query size
        """
        self.cur.execute(query)
        data = self.cur.fetchall()
        return data
