from src.models.base_model import BaseModel
from src.config.settings import GROQ_API_URL, GROQ_API_KEY

class GroqModel(BaseModel):
    """
    Class for interacting with the Groq API.
    Inherits from BaseModel.
    """
    
    def __init__(self):
        super().__init__(api_url=GROQ_API_URL, api_key=GROQ_API_KEY)

    def process_request(self, prompt:dict, max_tokens: int = 500, temperature: float = 0, model:str="llama3-8b-8192", additional_payload:dict={}):
        """
        Process a request to the Groq API using a generated prompt.
        """
        prompt_system = prompt["system"]
        prompt_user = prompt["user"]
        
        payload = {
            "model": model,
                "messages": [
                {
                "role": "system",
                "content": prompt_system
                },
                {"role": "user", "content": prompt_user}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            **additional_payload
        }

        response = self.request("chat/completions", payload)
        return response["choices"][0]["message"]["content"]