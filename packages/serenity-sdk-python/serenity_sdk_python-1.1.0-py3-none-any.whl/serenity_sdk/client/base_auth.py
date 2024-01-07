from abc import ABC, abstractmethod


class AuthToken:
    """
    Internal Class to hold the credential's access token and expiry time
    """
    def __init__(self):
        self.token = None
        self.expires_on = None


class BaseAuthCredential(ABC):

    @abstractmethod
    def get_token(self) -> AuthToken:
        pass
