# gervasebots/client.py
import requests
from .errors import *
from .checks import *
from .creds import *

class Client:
    def __init__(self, bot, api_token, post_success_callback=None):
        
        self._post_success_callback = post_success_callback
        check_valid_api_token(api_token)


        self._is_closed = False
        self.bot = bot
        self.api_token = api_token

    def check_closed(self):
        """Check if the client is closed."""
        if self._is_closed:
            raise APIClientError("Client is closed.")

    def close(self):
        """Close the client."""
        self._is_closed = True

    @property
    def closed(self):
        return self._is_closed

    def get_bot_info(self):
        self.check_closed()

        headers = {
            'Authorization': f'APP {self.api_token}'
        }
        response = requests.get(f'{base_url}/api/bot', headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise APIClientError(f'Error {response.status_code}: {response.text}')

    def post_guild_count(self):
        """Update the guild count."""
        self.check_closed()

        headers = {
            'Authorization': f'APP {self.api_token}'
        }

        data = {
            'guild_count': len(self.bot.guilds)
        }

        response = requests.post(f'{base_url}/api/bot', json=data, headers=headers)

        if response.status_code != 200:
            raise APIClientError(f'Error {response.status_code}: {response.text}')
    
    def on_post_success(self):
        """Execute the callback on successful post."""
        if self._post_success_callback:
            self._post_success_callback()

    