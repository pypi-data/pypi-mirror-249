import requests
from typing import List, Optional
from pydantic import BaseModel
import json
import warnings


warnings.filterwarnings("ignore", category=UserWarning)


ENDPOINT = "https://interactions-s7cwzbgfoq-uc.a.run.app"
EVALUATOR_ENDPOINT = "https://evaluate-s7cwzbgfoq-uc.a.run.app"

class ScorePayload(BaseModel):
    """Pydantic model representing a score payload."""
    val: int
    name: str

class InteractionPayload(BaseModel):
    """Pydantic model representing an interaction payload."""
    input: str = ""
    output: str = ""
    scores: List[ScorePayload] = []
    model_name: str = ""
    session_id: Optional[str] = ""

class Gavel:
    """Gavel class for managing interactions with the API."""
    def __init__(self, api_key):
        """
        Initialize Gavel instance.

        Parameters:
        - api_key (str): The API key for authentication.
        """
        self.api_key = api_key
        self.endpoint = ENDPOINT


    def session(self, model_name, id=None):
        """
        Create a session for a specific model.

        Parameters:
        - model_name (str): The name of the model for the session.

        Returns:
        - Session: A Session instance for the specified model.
        """
        return Session(model_name, api_key=self.api_key, id=id, endpoint=self.endpoint)
    
    def autoscore(self, input:str, output:str, evaluator:str):
        """
        Score an interaction.

        Parameters:
        - input (str): The input for the interaction.
        - output (str): The output for the interaction.

        Returns:
        - dict: The response from the API.
        """
       
        # Replace with the deployed cloud function's URL

        # Sample data to send - replace with your actual data structure
        data = {
            "input":input,
            "output":output,
            "evaluator":evaluator
        }

        # Convert the Python dictionary to a JSON string
        payload = json.dumps(data)
        # Set headers to specify the content type
        headers = {
            'Content-Type': 'application/json',
        }

        # Send the POST request with the payload
        response = requests.post(EVALUATOR_ENDPOINT, headers=headers, data=payload)

        return response



class Session:
    """Session class representing a session with a specific model."""
    def __init__(self, model_name: str, id:Optional[str],  api_key: str, endpoint:str):
        """
        Initialize Session instance.

        Parameters:
        - model_name (str): The name of the model for the session.
        - api_key (str): The API key for authentication.
        - id (Optional[str]): The session ID (default is None).
        """
        self.model_name = model_name
        self.id = id
        self.api_key = api_key
        self.endpoint = endpoint

    def interact(self):
        """
        Create an interaction within the session.

        Returns:
        - Interaction: An Interaction instance for the session.
        """
        return Interaction(api_key=self.api_key, session_id=self.id, model_name=self.model_name, endpoint=self.endpoint)

class Interaction:
    """Interaction class representing an interaction within a session."""
    def __init__(self, api_key: str, model_name: str,  endpoint:str, session_id=None):
        """
        Initialize Interaction instance.

        Parameters:
        - api_key (str): The API key for authentication.
        - model_name (str): The name of the model for the interaction.
        - session_id (Optional[str]): The session ID (default is None).
        """
        self.api_key = api_key
        self.payload = InteractionPayload(model_name=model_name, session_id=session_id)
        self.endpoint = endpoint

    def input(self, model_input):
        """
        Set the input for the interaction.

        Parameters:
        - model_input (str): The input for the interaction.
        """
        self.payload.input = model_input

    def output(self, model_output):
        """
        Set the output for the interaction.

        Parameters:
        - model_output (str): The output for the interaction.
        """
        self.payload.output = model_output

    def score(self, name, value):
        """
        Add a score to the interaction.

        Parameters:
        - name (str): The name of the score.
        - value: The value of the score.
        """
        score = ScorePayload(name=name, val=value)
        self.payload.scores.append(score)

    def log(self):
        """
        Submit the interaction to the API.

        Returns:
        - dict: The response from the API.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        response = requests.post(self.endpoint, json=self.payload.dict(), headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to submit interaction. Status Code: {response.status_code}, Response: {response.text}")
