from src.models.base_model import BaseModel

class SummarizationService:
    def __init__(self, model:BaseModel):
        self.model = model

    def summarize(self, text:str, max_token:int=500, temperature:float=0):
        """
        Perform text Summarization.
        :param text: The text to summarize.
        :param max_tokens: The maximum number of tokens to generate.
        :param temperature: The temperature for randomness in results.
        """
        prompt = {}
        prompt["system"] = (
            "Your task is to analyze the following text and respond in the same language as the text. "
            "If the text is in Chinese, your response must be in Chinese. If the text is in another language, respond in that language. "
            "Provide only the following details in your response: "
            "Title: [Provide a suitable title for the text] "
            "Key Words: [Extract and list the key words] "
            "Summary: [Write a concise summary of the text]."
        )

        

        prompt["user"] = f"Text: {text}"
        response = self.model.process_request(prompt, max_token, temperature, model="llama3-70b-8192")
        
        return response