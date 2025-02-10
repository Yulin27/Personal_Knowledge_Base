from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def generate_embedding(self, text: str):
        """
        Generate an embedding for the text.
        """
        embedding = self.model.encode(text)
        return embedding

    def cosine_similarity(self, embedding1: np.array, embedding2: np.array):
        """
        Calculate the cosine similarity between two embeddings.
        """
        similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
        return similarity
