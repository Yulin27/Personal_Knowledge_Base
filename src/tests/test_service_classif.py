import unittest
from unittest.mock import MagicMock
from src.services.classification import ClassificationService
from src.models.groq_model import GroqModel


# Unit test for ClassificationService
class TestClassificationService(unittest.TestCase):

    def setUp(self):
        # Mock the BaseModel
        self.mock_model = MagicMock(spec=GroqModel)

        # Define the mock return value for process_request
        self.mock_model.process_request.return_value = "Technology"

        # Initialize ClassificationService with the mock model
        self.classification_service = ClassificationService(model=self.mock_model)

    def test_classify(self):
        # Define test data
        text = "Artificial intelligence is transforming the world."
        labels = ["Technology", "Health", "Finance", "Education"]

        # Call the classify method
        result = self.classification_service.classify(text=text, labels=labels)
        # Assert the result is as expected
        self.assertEqual(result, "Technology")

        # Ensure the request method was called with the correct prompt
        prompt = {}
        labels_str = ', '.join(labels)
        prompt["system"] = f"Your task is to classify the following text into one of the categories: {labels_str}.Given the text, which category does it belong to? Response only with the category name."
        prompt["user"] = f"Text: {text}"
        expected_prompt = prompt
        self.mock_model.process_request.assert_called_with(expected_prompt, 100, 0)

    def test_classify_with_real_model(self):
        # Initialize the real model (use real API credentials if necessary)
        real_model = GroqModel()
        classification_service = ClassificationService(model=real_model)

        # Define test data
        text = "Artificial intelligence is transforming the world."
        labels = ["Technology", "Health", "Finance", "Education"]

        # Call the classify method
        result = classification_service.classify(text=text, labels=labels)

        # Print or assert the result
        print("Real model output:", result)
        self.assertEqual(result, "Technology")

if __name__ == "__main__":
    unittest.main()



    
