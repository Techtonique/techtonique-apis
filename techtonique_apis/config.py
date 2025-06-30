import os
from dotenv import load_dotenv

BASE_URL = "https://www.techtonique.net"
# BASE_URL = "http://127.0.0.1:8000"


def get_token(token=None):
    """
    Retrieve the API token, either from the environment or user input.

    Parameters:
    -----------
    token : str
        Token provided as a parameter (default is None).

    Returns:
    --------
    str
        A valid API token.
    """
    if token:
        return token

    # Load environment variables from .env if available
    load_dotenv()
    token = os.getenv("TECHTONIQUE_TOKEN")

    if not token:
        # Prompt user for token if not found in environment
        token = getpass.getpass(
            "Enter your token (from https://www.techtonique.net/token): ")

    if not token:
        raise ValueError("API token is required but was not provided.")

    return token
