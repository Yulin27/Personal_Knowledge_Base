from src.config.settings import DATABASE
from src.database.postgres import Postgres
import logging

logging.basicConfig(
    filename="logs/app.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def create_table():

    # Initialize the Postgres database connection
    postgres = Postgres()
    postgres.connect()

    # Create the table in the Postgres database
    table_name = "knowledge_base"
    columns = {
        "id": "SERIAL PRIMARY KEY",
        "title": "VARCHAR(255) NOT NULL",
        "keywords": "VARCHAR(255)[]",
        "summary": "TEXT",
        "category": "VARCHAR(100)",
        "text": "TEXT",
        "embedding": "VECTOR(384)",
        "created_at": "TIMESTAMP DEFAULT NOW()",
        "updated_at": "TIMESTAMP DEFAULT NOW()"
    }

    try:
        postgres.create_table(table_name, columns)
    except Exception as e:
        logging.error(f"Error creating table: {e}")
        

    # Close the connection to the Postgres database
    postgres.close()


def main():
    create_table()

if __name__ == "__main__":
    main()