from django.conf import settings
from django.utils import timezone
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from .models import Token


class Deviantart(object):
    oauth = None
    url = 'https://www.deviantart.com/api/v1/oauth2/'
    auth_url = None
    state = None
    scope = getattr(settings, 'DEVIANTART_SCOPE', ['browse'])
    # allow_user: True-> Every user has a deviantart token
    #             False-> Default
    allow_user = getattr(settings, 'DEVIANTART_ALLOW_USER', False)
    # auth_User: Django user authentificated
    auth_user = None

    def __init__(self, redirect_url=None, auth_user=None):
        self.auth_user = auth_user
        
        if self.allow_user:
            # If DEVIANTART_ALLOW_USER= TRUE
            if not self.auth_user.is_authenticated:
                #But user given is none 
                raise Exception("Deviantart:Trying to get token without auth.")
            # The token must be filtered by the user authenticated
            token = Token.objects.filter(user=auth_user).last()
        else:
            # Default mode
            token = Token.objects.filter(client_id=settings.DEVIANTART_CLIENT_ID).last()

        if token and redirect_url is None:

            t = {
                'refresh_token': token.refresh_token,
                'access_token': token.access_token,
                'expires_in': (token.expires_at - timezone.now()).total_seconds() - 60
            }

            extra = {
                'client_id': settings.DEVIANTART_CLIENT_ID,
                'client_secret': settings.DEVIANTART_CLIENT_SECRET,
            }

            client = BackendApplicationClient(
                client_id=settings.DEVIANTART_CLIENT_ID
            )

            self.oauth = OAuth2Session(client,
                                       token=t,
                                       auto_refresh_kwargs=extra,
                                       auto_refresh_url='https://www.deviantart.com/oauth2/token',
                                       token_updater=self.save_token
                                       )
        else:
            self.oauth = OAuth2Session(client_id=settings.DEVIANTART_CLIENT_ID,
                                       redirect_uri=redirect_url,
                                       scope=self.scope)

            self.auth_url, self.state = self.oauth.authorization_url(
                'https://www.deviantart.com/oauth2/authorize'
            )

    def fetch_token(self, code):
        self.oauth.fetch_token(
            token_url='https://www.deviantart.com/oauth2/token',
            client_secret=settings.DEVIANTART_CLIENT_SECRET,
            client_id=settings.DEVIANTART_CLIENT_ID,
            code=code,
        )

        self.save_token()

    def save_token(self, *args):
        # If DEVIANTART_ALLOW_USER= TRUE,  save the user, if not save Null
        user = self.auth_user if self.allow_user else None
        
        t, created = Token.objects.update_or_create(
            client_id=settings.DEVIANTART_CLIENT_ID,
            user=user,
            defaults=dict(
                access_token=self.oauth.token['access_token'],
                expires_at=timezone.make_aware(timezone.datetime.fromtimestamp(self.oauth.token['expires_at'])),
                refresh_token=self.oauth.token['refresh_token']
        )
        )

        return t

    def get(self, endpoint):

        return self.oauth.get(
            self.url + endpoint
        ).json()
