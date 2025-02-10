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
        text = """A transformer is a deep learning architecture that was developed by researchers at Google and is based on the multi-head attention mechanism, which was proposed in the 2017 paper "Attention Is All You Need".[1] Text is converted to numerical representations called tokens, and each token is converted into a vector via lookup from a word embedding table.[1] At each layer, each token is then contextualized within the scope of the context window with other (unmasked) tokens via a parallel multi-head attention mechanism, allowing the signal for key tokens to be amplified and less important tokens to be diminished.

        Transformers have the advantage of having no recurrent units, therefore requiring less training time than earlier recurrent neural architectures (RNNs) such as long short-term memory (LSTM).[2] Later variations have been widely adopted for training large language models (LLM) on large (language) datasets, such as the Wikipedia corpus and Common Crawl.[3]

        Transformers were first developed as an improvement over previous architectures for machine translation,[4][5] but have found many applications since. They are used in large-scale natural language processing, computer vision (vision transformers), reinforcement learning,[6][7] audio,[8] multimodal learning, robotics,[9] and even playing chess.[10] It has also led to the development of pre-trained systems, such as generative pre-trained transformers (GPTs)[11] and BERT[12] (bidirectional encoder representations from transformers).

        """
        
        labels = ["Technology", "Health", "Finance", "Education"]

        # Call the classify method
        result = classification_service.classify(text=text, labels=labels)

        # Print or assert the result
        print("Real model output:", result)
        self.assertEqual(result, "Technology")

if __name__ == "__main__":
    unittest.main()



    
