from datetime import datetime
from typing import Dict

from serenity_sdk.client.auth0_client_cred_auth import Auth0ClientCredAuth
from serenity_sdk.client.auth0_device_auth import Auth0DeviceAuth
from serenity_sdk.client.base_auth import AuthToken, BaseAuthCredential
from serenity_sdk.config import ConnectionConfig

SERENITY_CLIENT_ID_HEADER = 'X-Serenity-Client-ID'


class AuthHeaders:
    """
    Helper object that carries all the headers required for API authentication and authorization.
    """
    def __init__(self, credential: BaseAuthCredential):
        """
        Creates an initial access token using the given credentials and scopes.

        :param credential: the credential object that returns the access token
        """
        self.credential = credential

        self.access_token = AuthToken()
        self.ensure_not_expired()

    def ensure_not_expired(self):
        """
        Check whether we need to refresh the bearer token now.
        """

        # expired is true if access_token.token exists with a Non-None value for attribute token and expires_on is less
        # than current time
        expired = (self.access_token is None or self.access_token.token is None or
                   self.access_token.expires_on < datetime.now().timestamp())
        if expired:
            self._refresh_token()

    def get_http_headers(self) -> Dict[str, str]:
        """
        Gets the current set of headers including latest Bearer token for authentication.

        :return: a mapping between HTTP header and header value
        """
        self.http_headers = {'Authorization': f"Bearer {self.access_token.token}"}
        return self.http_headers

    def _refresh_token(self):
        self.access_token = self.credential.get_token()
        self.http_headers = {'Authorization': f"Bearer {self.access_token.token}"}


def get_credential_user_app(config: ConnectionConfig) -> BaseAuthCredential:
    """
    Standard mechanism to acquire a credential for accessing the Serenity API. You
    can create one or more user applications using the Serenity Admin screen, and
    as part of setup you will be given the application's client ID and secret.

    :param config: Serenity API Management API configuration from `load_local_config()`
    :return: the Auth0 credential object including token and expiry
    """
    if config.user_client_id:
        return Auth0DeviceAuth(config)
    else:
        return Auth0ClientCredAuth(config)


def create_auth_headers(credential: BaseAuthCredential) -> AuthHeaders:
    """
    Helper function for the standard requests module to construct the appropriate
    HTTP headers for a given set of API endpoints and a user application's
    client ID. The latter is used by Serenity to distinguish between different client
    applications on the backend.
    """
    return AuthHeaders(credential)
