from abc import ABC, abstractmethod
import logging
import requests


class BaseModel(ABC):
    """
    Base class for all models that interact with APIs.
    Includes functionality for making requests to APIs and logging.
    """

    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def log(self, message: str):
        """
        Log a message.
        """
        logging.info(message)

    def request(self, endpoint: str, payload: dict):
        """
        Make a request to the API and handle response.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(f"{self.api_url}/{endpoint}", headers=headers, json=payload)
            self.log(f"Request to {self.api_url}/{endpoint}")

            if response.status_code == 200:
                self.log(f"Response: {response.json()}")
                return response.json()

            else:
                self.log(f"Error {response.status_code}: {response.text}")
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            self.log(f"Request error: {e}")
            raise

    @abstractmethod
    def process_request(self, *args, **kwargs):
        """
        Abstract method for generating output from the API
        """
        pass

        