from src.models.base_model import BaseModel

class ClassificationService:
    def __init__(self, model:BaseModel):
        self.model = model

    def classify(self, text:str, labels:list, max_token:int=50, temperature:float=0):
        """
        Perform text classification.
        :param text: The text to classify.
        :param labels: A list of possible labels.
        :param max_tokens: The maximum number of tokens to generate.
        :param temperature: The temperature for randomness in results.
        """
        labels_str = ', '.join(labels)
        prompt = {}
        prompt["system"] = f"Your task is to classify the following text into one of the categories: {labels_str}.Given the text, which category does it belong to? Response only with the category name."
        prompt["user"] = f"Text: {text}"
        response = self.model.process_request(prompt, max_token, temperature)
        return response