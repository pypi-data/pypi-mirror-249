import ipywidgets as widgets

from IPython.display import clear_output, display
from serenity_sdk.api.provider import SerenityApiProvider

from serenity_sdk.client import SerenityClient
from serenity_sdk.config import load_local_config


class ConnectWidget:

    def __init__(self, config_id: str = None):
        self.prompt = widgets.Label(value='Specify config filename located in your ~/.serenity folder \
                                     (exclude .json extension):')
        self.widget_api_config = widgets.Text(description='API Config:')
        self.widget_connect = widgets.Button(description='Connect',
                                             disabled=False,
                                             button_style='',
                                             tooltip='Connect to Serenity',
                                             icon='link')
        self.widget_out = widgets.Output()

        self.api: SerenityApiProvider = None
        self.env_value = None

        self.widget_connect.on_click(self.connect_button_clicked)

        # display
        hbox = widgets.HBox([self.widget_api_config])
        vbox = widgets.VBox([self.prompt, hbox, self.widget_connect, self.widget_out])

        display(vbox)

        if config_id is not None:
            self.widget_api_config.value = config_id
            self.widget_connect.click()

    def get_api(self) -> SerenityApiProvider:
        if self.api is None:
            raise ValueError("'api' is not yet set.")
        return self.api

    def get_client(self) -> SerenityClient:
        if self.client is None:
            raise ValueError("'client' is not yet set.")
        return self.client

    def connect_button_clicked(self, button):
        config_id = self.widget_api_config.value
        config = load_local_config(config_id)
        self.client = SerenityClient(config)
        self.api = SerenityApiProvider(self.client)

        with (self.widget_out):
            clear_output()
            print(f'Connecting to {config_id}: env={self.client.env}, '
                  f'URL={self.client.config.url}')
