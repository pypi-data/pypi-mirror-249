# gervasebots/checks.py
from .errors import APITokenError
import requests
from .creds import *

def check_valid_api_token(api_token):
    """Check if the API token is valid."""
    if not api_token:
        raise APITokenError("API token is required.")

    re = requests.get(f"{base_url}/api/check", headers={"Authorization": f"APP {api_token}"})
    
    if re.status_code == 200:
        return True
    else:
        raise APITokenError("Token is Incorrect.")
