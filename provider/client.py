import requests
import json
from django.conf import settings
from collections import OrderedDict
from urllib.parse import quote, urlencode
from django.utils.http import urlencode

from allauth.socialaccount.providers.oauth2.client import (
    OAuth2Client,
    OAuth2Error,
)

class FortyTwoOAuth2Client(OAuth2Client):

    base_url = f'{settings.OAUTH_SERVER_BASEURL}/oauth/authorize'
    token_url = f'{settings.OAUTH_SERVER_BASEURL}/oauth/token'
    client_id = 'u-s4t2ud-c54860141cd7e4afbb2b7f4f6fdaed8483360fba16e5acf438a021964386f8e6'
    client_secret = "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"
    redirect_uri = 'http://127.0.0.1:8000/42/login/callback/'
    response_type = 'code'
    
    def get_redirect_url(self, authorization_url, extra_params):
        
        params = {
            'client_id': self.client_id,
            'redirect_uri': quote(self.redirect_uri, safe=''),
            'response_type': self.response_type,
        }
        if self.state:
            params["state"] = self.state
        params.update(extra_params)
        print(params)
        return "%s?%s" % (authorization_url, urlencode(params))

    def get_access_token(self, code):
        """
        Request access token from the provider using the code returned by the
        Returns:
            {
                "access_token": "cf04dea4652cac698153b0a33321f97ec60103f38af469ac86586ca13b962fc7",
                "token_type": "bearer",
                "expires_in": 7200,
                "scope": "public",
                "created_at": 1712043465,
                "secret_valid_until": 1714314643
            }
        """

        data = {
            "grant_type": "client_credentials",
            "client_id": self.consumer_key,
            "client_secret": self.consumer_secret,
        }

        resp = requests.request(self.token_url, method='POST', data=data)

        access_token = None
        if resp.status_code == 200:
            access_token = resp.json()['access_token']
        else:
            raise OAuth2Error("Error retrieving app access token: %s" % resp.content)
        
        return access_token['access_token']
