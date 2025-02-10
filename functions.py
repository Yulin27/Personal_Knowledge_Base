from src.config.settings import DATABASE
from src.database.postgres import Postgres
import logging
from src.document.document import Document
from src.database.postgres import Postgres


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
        "name": "VARCHAR(255) NOT NULL",
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

def insert_doc(text: str, labels:list, name: str = None, keywords: list = None, summary: str = None, category: str = None):
    """
    Insert a document into the Postgres database.
    """
    # Initialize the document
    document = Document(text=text, name=name, keywords=keywords, summary=summary, category=category)
    # Generate information about the document
    document.generate_info(labels=labels)
    # Insert the document into the Postgres database
    postgres = Postgres()
    postgres.connect()
    postgres.insert_one_data(table_name="knowledge_base", data=document.to_dict())
    postgres.close()


