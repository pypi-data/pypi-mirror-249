import ipywidgets as widgets
from typing import Optional
import numpy as np
import pandas as pd
from datetime import datetime

from serenity_sdk.api.provider import SerenityApiProvider
from .reference_data import get_predefined_option_infos


class VersionTimeChooser:
    def __init__(self, versions: list, id_key: str):

        self.versions = versions
        self.id_key = id_key
        self.name_to_id = {v.definition.display_name: getattr(v.definition, id_key) for v in versions}
        self.available_id_times = {
            getattr(v.definition, id_key):
            sorted([as_of_time.replace(tzinfo=None) for as_of_time in v.as_of_times], reverse=True)
            for v in versions}

        self.widget_name = widgets.Dropdown(
            options=[name for name in self.name_to_id],
            value=None,
            description='Name')

        self.widget_id = widgets.Text(
            value='',
            description='Id (uuid)',
            disabled=False)

        self.widget_as_of_time = widgets.Dropdown(
            options=[],
            disabled=False,
            description='As-of Time')
        self.id_selected = None
        self.widget_name.observe(self.__name_changed, names='value')

        # set the first element into name box
        self.widget_name.value = list(self.name_to_id)[0]

    def __name_changed(self, wb):
        name = self.widget_name.value
        id = self.name_to_id[name]
        self.widget_as_of_time.options = self.available_id_times[id]
        self.widget_id.value = str(id)
        self.selected_id = id

    def get_widget_to_display(self):
        return widgets.VBox(
            [widgets.HBox([self.widget_name, self.widget_as_of_time]),
             self.widget_id])

    def get_id_as_of_time(self):
        return self.selected_id, self.widget_as_of_time.value


class YieldCurveVersionTimeChooser(VersionTimeChooser):
    def __init__(self,
                 api: Optional[SerenityApiProvider] = None,
                 start_datetime: Optional[datetime] = None,
                 end_datetime: Optional[datetime] = None,
                 versions: Optional[list] = None):

        if api is not None:
            versions = api.pricer().get_available_yield_curve_versions(
                start_datetime=start_datetime, end_datetime=end_datetime)
        else:
            versions = versions

        super().__init__(versions, 'yield_curve_id')


class VolatilitySurfaceVersionTimeChooser(VersionTimeChooser):
    def __init__(self, api: Optional[SerenityApiProvider] = None,
                 start_datetime: Optional[datetime] = None,
                 end_datetime: Optional[datetime] = None,
                 versions: Optional[list] = None):

        if api is not None:
            versions = api.pricer().get_available_volatility_surface_versions(
                start_datetime=start_datetime, end_datetime=end_datetime)
        else:
            versions = versions
        super().__init__(versions, 'vol_surface_id')


class OptionChooser:

    def __init__(self,
                 api: Optional[SerenityApiProvider] = None,
                 option_data: Optional[pd.DataFrame] = None):
        """
        Specify either api (to retrieve options from Serenity database) or option_data (to use user's own data)

        :param api: Serenity api provider, defaults to None
        :param option_data: dataframe of options, defaults to None
        """

        if api is not None:
            self.data = get_predefined_option_infos(api)
        else:
            self.data = option_data.reset_index().copy()
        # add option_type in string
        self.data['option_type_str'] = self.data['option_type'].apply(lambda x: x.name)

        underlier_asset_symbols = np.sort(self.data['native_symbol_underlier'].unique())

        self.widget_underlier_asset_symbol = widgets.Dropdown(
            options=underlier_asset_symbols,
            value=None,
            description='Underlier Asset'
        )

        self.widget_expiry = widgets.Dropdown(
            options=[],
            disabled=False,
            description='Expiry'
        )

        self.widget_strike = widgets.Dropdown(
            options=[],
            disabled=False,
            description='Strike'
        )

        self.widget_option_type = widgets.Dropdown(
            options=[],
            disabled=False,
            description='Type'
        )

        self.cols_widgets = ['native_symbol_underlier', 'expiry_datetime', 'strike_price', 'option_type_str']
        self.list_widgets = [self.widget_underlier_asset_symbol,
                             self.widget_expiry, self.widget_strike, self.widget_option_type]

        self.widget_underlier_asset_symbol.observe(self.__widget_underlier_asset_symbol_changed, names='value')
        self.widget_expiry.observe(self.__widget_expiry_changed, names='value')
        self.widget_strike.observe(self.__widget_strike_changed, names='value')

        # set the initial symbol
        self.widget_underlier_asset_symbol.value = underlier_asset_symbols[0]
        self.widget_expiry.value = self.widget_expiry.options[-1]

    def __set_mid_strike(self):
        num_strikes = len(self.widget_strike.options)
        self.widget_strike.value = self.widget_strike.options[num_strikes//2]

    def __match(self, level=4):

        df = self.data
        for i in range(level):
            df = df[df[self.cols_widgets[i]] == self.list_widgets[i].value].copy()
        return df

    def __update_widgets(self, level):

        for i in range(level+1, len(self.cols_widgets)):
            df = self.__match(i)
            self.list_widgets[i].options = list(np.sort(df[self.cols_widgets[i]].unique()))

    def __widget_underlier_asset_symbol_changed(self, wb):

        self.__update_widgets(0)
        self.__set_mid_strike()

    def __widget_expiry_changed(self, wb):
        self.__update_widgets(1)
        self.__set_mid_strike()

    def __widget_strike_changed(self, wb):
        self.__update_widgets(2)

    def get_widget_to_display(self):
        return widgets.VBox([self.widget_underlier_asset_symbol, self.widget_expiry,
                             self.widget_strike, self.widget_option_type])

    def get_selected_option(self) -> pd.Series:

        df = self.__match(4)

        if df.shape[0] != 1:
            raise ValueError('Something went wrong. Check your selection')
        else:
            dict = df.iloc[0].to_dict()
            del dict['option_type_str']
            return dict
