import time

from auth0.authentication import GetToken
from serenity_sdk.client.base_auth import AuthToken, BaseAuthCredential
from serenity_sdk.config import ConnectionConfig


class Auth0ClientCredAuth(BaseAuthCredential):
    """
    Class to authenticate with the Serenity API using the Auth0 Client Credentials Flow.  This class is for internal
    use and normally you should not need to instantiate it.
    """
    def __init__(self, config: ConnectionConfig):
        """
        :param config: The loaded connection configuration params to use for the authentication process
        """
        self.access_token = AuthToken()
        self._config = config

    def get_token(self) -> AuthToken:
        """
        Gets an access token from the Auth0 API following the client credentials flow.
        """
        domain = self._config.domain
        client_id = self._config.client_id
        client_secret = self._config.client_secret
        aud = self._config.user_audience
        token = GetToken(domain, client_id, client_secret)
        access_token = token.client_credentials(aud)
        self.access_token.token = access_token['access_token']
        expires_on = int(time.time()) + int(access_token['expires_in'])

        print("Access Confirmed!")
        expires_on_display = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime(expires_on))
        current_time = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime(time.time()))
        print(f"- Auth code expires: {expires_on_display} (Current time: {current_time})")

        self.access_token.expires_on = expires_on

        # return a new object with properties access_token and access_token_expiry
        return self.access_token
