import json
import time
from http.client import HTTPSConnection

from serenity_sdk.client.base_auth import AuthToken, BaseAuthCredential
from serenity_sdk.config import ConnectionConfig


class Auth0DeviceAuth(BaseAuthCredential):
    """
    Class to authenticate with the Serenity API using the Auth0 Device Code Flow.  This class is for internal
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
        Gets an access token from the Auth0 API. This method will block until either the user has completed the
        authentication process or a timeout has occurred.
        """
        conn = HTTPSConnection(f"{self._config.domain}")
        payload = f"client_id={self._config.user_client_id}&audience={self._config.user_audience}"  # noqa: E501 - URL definition

        headers = {'content-type': "application/x-www-form-urlencoded"}
        conn.request("POST", "/oauth/device/code", payload, headers)

        res = conn.getresponse()
        data = res.read()

        code_request_res = json.loads(data.decode("utf-8"))
        device_code = code_request_res["device_code"]

        # If expires_in property is not a number, raise an error
        if not isinstance(code_request_res["expires_in"], int):
            raise ValueError(f"expires_in property is not a number: {code_request_res['expires_in']}")
        print(f"Please visit {code_request_res['verification_uri_complete']} to complete the authentication process...")

        time.sleep(5)
        payload = f"grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Adevice_code&device_code={device_code}&client_id={self._config.user_client_id}"  # noqa: E501 - URL definition

        poll_count = 0
        max_poll = 18
        while True:
            poll_count += 1
            conn.request("POST", "/oauth/token", payload, headers)
            res = conn.getresponse()
            data = res.read()
            token_res = json.loads(data.decode("utf-8"))
            if "error" in token_res and token_res["error"] == "authorization_pending":
                seconds_left = max_poll * 5 - poll_count * 5
                if seconds_left <= 0:
                    print("Error: Timeout waiting for authorization.  Feel free to try again...")
                    raise ValueError("Timeout waiting for authorization")
                print(f"Waiting for authorization... ({seconds_left} seconds left)")
                time.sleep(5)
            elif "error" in token_res:
                raise ValueError(f"Error in response: {token_res['error']}")
            else:
                break
        print("Access Confirmed!")

        expires_on = int(time.time()) + int(token_res["expires_in"])

        self.access_token.token = token_res["access_token"]
        expires_on_display = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime(expires_on))
        current_time = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime(time.time()))
        print(f"- Auth code expires: {expires_on_display} (Current time: {current_time})")

        self.access_token.expires_on = expires_on

        # return a new object with properties access_token and access_token_expiry
        return self.access_token
