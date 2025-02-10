from src.services.summarization import SummarizationService
from src.services.classification import ClassificationService
from src.utils.parse import parse_title_kw_summary 
from src.services.embedding import EmbeddingService
import uuid
from src.config.settings import DATABASE
from src.models.groq_model import GroqModel

class Document:
    def __init__(self, text: str, title: str = None, keywords: list = None, summary: str = None, category: str = None):
        self.text = text
        self.title = title
        self.keywords = keywords
        self.summary = summary
        self.embedding = None
        self.category = category

    def __str__(self):
        string = f"""title: {self.title}\n
                    Keywords: {self.keywords}\n
                    Summary: {self.summary}\n
                    Category: {self.category}\n
                    Text: {self.text}\n
                    Embedding: {self.embedding}\n
                    """
        return string


    def generate_info(self, labels: list):
        """
        Generate information about the document.
        """
        # Summarize the text
        model = GroqModel()
        summarization_service = SummarizationService(model=model)
        info = summarization_service.summarize(self.text)
        # Parse the title, keywords and summary
        parsed_info = parse_title_kw_summary(info)
        self.title = parsed_info["title"]
        self.keywords = parsed_info["keywords"]
        self.summary = parsed_info["summary"]
        

        # Classify the text
        classification_service = ClassificationService(model=model)
        self.category = classification_service.classify(self.text, labels)

        # Generate the embedding
        embedding_service = EmbeddingService()
        self.embedding = embedding_service.generate_embedding(self.text)

    def to_dict(self):
        """
        Convert the document to a dictionary.
        """
        return {
            "title": self.title,
            "keywords": self.keywords,
            "summary": self.summary,
            "category": self.category,
            "text": self.text,
            "embedding": self.embedding.tolist()
        }

    def from_dict(self, data: dict):
        """
        Load the document from a dictionary.
        """
        self.title = data["title"]
        self.keywords = data["keywords"]
        self.summary = data["summary"]
        self.category = data["category"]
        self.text = data["text"]
        self.embedding = data["embedding"]

    def insert_bd(self, db, table_name):
        """
        Insert the document into the database.
        """
        db.insert_one_data(table_name, self.to_dict())

    def update_bd(self, db, table_name):
        """
        Update the document in the database.
        """
        db.update_data(table_name, self.to_dict(), f"id = '{self.id}'")

    def delete_bd(self, db, table_name):
        """
        Delete the document from the database.
        """
        db.delete_data(table_name, f"id = '{self.id}'")
        