import requests

from django.urls import reverse
from django.conf import settings
from allauth.account import app_settings
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)
from allauth.socialaccount.providers.oauth2.client import (
    OAuth2Error,
)
from allauth.utils import build_absolute_uri

from .client import FortyTwoOAuth2Client
from .provider import FortyTwoProvider


class FortyTwoOAuth2Adapter(OAuth2Adapter):
    provider_id = FortyTwoProvider.id
    
    access_token_url = f'{settings.OAUTH_SERVER_BASEURL}/oauth/token'
    profile_url = f'{settings.OAUTH_SERVER_BASEURL}/v2/me'
    authorize_url = f'{settings.OAUTH_SERVER_BASEURL}/oauth/authorize'

    def complete_login(self, request, app, token, **kwargs):
        openid = kwargs.get("response", {}).get("openid")
        resp = requests.get(
            self.profile_url,
            headers ={'Content-Type': 'application/json',
                      'Authorization': f'Bearer {token}',
                      'Accept':'application/json'},
        )
        extra_data = resp.json()
        print(extra_data)
        if extra_data['code'] != 0:
            raise OAuth2Error("Error retrieving code: %s" % resp.content)
        extra_data = extra_data['data']

        return self.get_provider().sociallogin_from_response(request, extra_data)


class FortyTwoOAuth2ClientMixin(object):
    def get_client(self, request, app):
        callback_url = reverse(self.adapter.provider_id + "_callback")
        protocol = (
            self.adapter.redirect_uri_protocol or app_settings.DEFAULT_HTTP_PROTOCOL
        )
        callback_url = build_absolute_uri(request, callback_url, protocol=protocol)
        print(callback_url)
        provider = self.adapter.get_provider()
        scope = provider.get_scope(request)
        client = FortyTwoOAuth2Client(
            request,
            app.client_id,
            app.secret,
            self.adapter.access_token_method,
            self.adapter.access_token_url,
            callback_url,
            scope,
        )
        print(client)
        return client


class FortyTwoOAuth2LoginView(FortyTwoOAuth2ClientMixin, OAuth2LoginView):
    pass


class FortyTwoOAuth2CallbackView(FortyTwoOAuth2ClientMixin, OAuth2CallbackView):
    pass


oauth2_login = FortyTwoOAuth2LoginView.adapter_view(FortyTwoOAuth2Adapter)
oauth2_callback = FortyTwoOAuth2CallbackView.adapter_view(FortyTwoOAuth2Adapter)