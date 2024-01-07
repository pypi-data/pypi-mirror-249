from datetime import datetime
from enum import Enum
from typing import Dict
from uuid import UUID
from pydantic import root_validator

from serenity_types.utils.serialization import CamelModel


class DatasetContent(Enum):
    """
    Enum for the available dataset contents.
    """
    CTM_PROJ_RATE = 'CTM_PROJ_RATE'
    CTM_BASIS = 'CTM_BASIS'


class DatasetContentTimeRange(CamelModel):
    """
    The dataset content availability datetime range.
    """

    min_datetime: datetime
    """
    The minimum / earliest dataset content datetime.
    """

    max_datetime: datetime
    """
    The maximum / latest dataset content datetime.
    """

    @root_validator
    def min_max_datetime(cls, values):
        if values['max_datetime'] < values['min_datetime']:
            raise ValueError(f"The specified min_datetime {values['min_datetime']} "
                             f"is later than max_datetime {values['max_datetime']}")
        return values


class DatasetContentInfo(CamelModel):
    """
    Model to represents dataset content information.
    """

    dataset_content: DatasetContent
    """
    The dataset content.
    """

    dataset_content_time_range: Dict[UUID, Dict[UUID, DatasetContentTimeRange]]
    """
    The dataset content availability datetime range.
    By underlier asset UUID and exchange UUID.
    """


class DatasetContentUrlAndToken(CamelModel):
    """
    Returns generated URL and SAS token to access dataset content.
    """

    dataset_content_info: DatasetContentInfo
    """
    Dataset content information.
    """

    root_url: str
    """
    Root URL to access Serenity.
    """

    prefix: str
    """
    Prefix for the dataset content location.
    """

    sas_token: str
    """
    Temporary SAS token to access Serenity.
    """

    full_list_files_url: str
    """
    The full URL to list dataset content files.
    i.e. {root_url}/{prefix}/{sas_token}.
    """
