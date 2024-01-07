import json
import os.path

from enum import Enum
from typing import Any, Optional


class Environment(Enum):
    """
    The operational environment (e.g. test vs. production) to use for connection purposes.
    """
    DEV = 'DEV'
    """
    Serenity's development environment
    """

    TEST = 'TEST'
    """
    Serenity's UAT (QA) environment
    """

    PROD = 'PROD'
    """
    Serenity's production environment
    """


class Region(Enum):
    """
    The regional installation of Serenity to use for connection purposes. Not currently used.
    """
    GLOBAL = ''
    EASTUS = 'eastus'
    EASTUS_2 = 'eastus2'


class ConnectionConfig:
    """
    The configuration object used to connect to Serenity. This object is used by the
    :class:`SerenityClient` to make API calls.

    .. seealso:: :func:`load_local_config`: utility function to load configs from local files
    """
    def __init__(self, domain: str, user_audience: str, url: str, env: Environment,
                 user_client_id: str = None, client_id: str = None, client_secret: str = None):
        """
        Builds a connection configuration from the given parameters.

        :param domain: the domain of the connection
        :param user_audience: the audience for user authentication
        :param user_client_id: the client ID for user authentication (required only for device code login)
        :param client_id: the client ID for client authentication (required only for client credentials login)
        :param client_secret: the client secret for client authentication (required only for client credentials login)
        :param url: the base URL of the Serenity API
        :param env: the environment to use for connection purposes (e.g. Environment.PROD)
        """
        if not domain:
            raise ValueError('domain must be specified')
        if not user_audience:
            raise ValueError('user_audience must be specified')
        if not url:
            raise ValueError('url must be specified')
        if not env:
            raise ValueError('env must be specified')
        if not user_client_id:
            if not client_id:
                raise ValueError('Either user_client_id or client_id must be specified')
            if not client_secret:
                raise ValueError('Either client_secret must be specified when using client_id')
        self.domain = domain
        self.user_audience = user_audience
        self.user_client_id = user_client_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.url = url
        self.env = env

    def get_url(self) -> str:
        """
        Gets the client-specific URL to use for all API requests
        """
        return self.url


class FileConnectionConfig(ConnectionConfig):
    """
    Internal class that handles interpreting the JSON config file generated
    by the Serenity UX API Management function. This class is for internal
    use and normally you should not need to instantiate it.

    .. seealso:: :func:`load_local_config`: utility function to load configs from local files
    """
    def __init__(self, config: Any, config_path: str):
        """
        Builds a connection configuration from a parsed JSON object.

        :param config: a parsed JSON object containing a Serenity API configuration
        :param config_path: for error messages -- the path from which the JSON was loaded
        """
        # basic validation, extract the schema version
        schema_version = FileConnectionConfig._validate_config_json(config, config_path)
        self.schema_version = schema_version

        # OK, we have a clean object, extract the core fields
        super().__init__(
            domain=config['domain'], user_audience=config['userAudience'],
            user_client_id=config.get('userClientId'), client_id=config.get('clientId'),
            client_secret=config.get('clientSecret'), url=config['url'], env=Environment(config['environment']))

    @staticmethod
    def _validate_config_json(config: Any, config_path: str) -> int:
        """
        Validates a config JSON from Serenity and ensures it matches the schema

        :param config: raw config JSON object
        :param config_path: file path from which the JSON was loaded; for error messages
        :return: the schema version loaded (currently 1 or 2)
        """
        critical_keys = ['schemaVersion']
        if not all(key in config for key in critical_keys):
            raise ValueError(f'{config_path} invalid. Required keys: {critical_keys}; got: {list(config.keys())}')
        schema_version = config['schemaVersion']
        if schema_version != 3:
            raise ValueError(f'At this time only schemaVersion == 3 is supported; '
                             f'{config_path} is version {schema_version}')
        device_code_required_keys = ['domain', 'userClientId', 'userAudience']
        client_cred_required_keys = ['domain', 'clientId', 'clientSecret', 'userAudience']
        if (not all(key in config for key in device_code_required_keys)
                and not all(key in config for key in client_cred_required_keys)):
            raise ValueError(
                f'{config_path} invalid. For Device Code Login Required keys: {device_code_required_keys};'
                f' Or Client Credentials Login Required keys: {client_cred_required_keys};'
                f' got: {list(config.keys())}')
        return schema_version


def load_local_config(config_id: str, config_dir: Optional[str] = None) -> FileConnectionConfig:
    """
    Helper function that lets you read a JSON config file with client ID and client secret from
    `$HOME/.serenity/${config_id}.json` on your local machine.

    :param config_id: short name of a configuration to load from `$HOME/.serenity`
    :param config_dir: optional override to load from a directory other than `$HOME/,serenity`
    :return: a populated, validated `ConnectionConfig` object to use with `SerenityClient`
    """

    if not config_dir:
        home_dir = os.path.expanduser('~')
        config_dir = os.path.join(home_dir, '.serenity')
    if not config_id.endswith('.json'):
        config_id += '.json'
    config_path = os.path.join(config_dir, config_id)

    # load and parse
    config_file = open(config_path)
    config = json.load(config_file)

    return FileConnectionConfig(config, config_path)
