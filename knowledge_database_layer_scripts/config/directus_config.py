"""
Directus client configuration and initialization
"""
import os
from dotenv import load_dotenv
from directus_sdk_py import DirectusClient

# Load environment variables
load_dotenv()

def get_directus_client():
    """
    Get a Directus client instance using token authentication
    Returns:
        DirectusClient: An authenticated Directus client
    """
    url = os.getenv("DIRECTUS_URL")
    token = os.getenv("DIRECTUS_TOKEN")
    
    if not url or not token:
        raise ValueError("DIRECTUS_URL and DIRECTUS_TOKEN must be set in .env file")
    
    return DirectusClient(url=url, token=token)

def get_directus_client_with_credentials():
    """
    Get a Directus client instance using email/password authentication
    Returns:
        DirectusClient: An authenticated Directus client
    """
    url = os.getenv("DIRECTUS_URL")
    email = os.getenv("DIRECTUS_EMAIL")
    password = os.getenv("DIRECTUS_PASSWORD")
    
    if not url or not email or not password:
        raise ValueError("DIRECTUS_URL, DIRECTUS_EMAIL, and DIRECTUS_PASSWORD must be set in .env file")
    
    client = DirectusClient(url=url)
    client.login(email=email, password=password)
    return client 