from typing import List, Dict
from uuid import UUID
from datetime import datetime
from serenity_types.utils.serialization import CamelModel
from serenity_types.valuation.core import NumberOrNone


class YieldSurfacesDatetimeRange(CamelModel):
    """
    Yield surface snapshots datetime range
    """

    underlier_asset_id: UUID
    """
    The underlier asset_id for this yield surface, e.g. BTC (78e2e8e2-419d-4515-9b6a-3d5ff1448e89).
    """

    min_snapshot_datetime: datetime
    """
    The minimum/earliest snapshot datetime for this yield surface.
    """

    max_snapshot_datetime: datetime
    """
    The maximum/latest snapshot datetime for this yield surface.
    """


class YieldSurfacesConfigs(CamelModel):
    """
    Serenity's configurations for yield surfaces.
    """

    supported_underlier_ids: List[UUID]
    """
    A list of supported underlier_asset_id.
    """

    max_allowed_snapshots: Dict[str, int]
    """
    The maximum allowed number of snapshots to be returned in one call.
    """


class YieldSurfaces(CamelModel):
    """
    Model representing yield surfaces.
    """

    yield_surface_id: UUID
    """
    Unique identifier for this yield surface.
    """

    underlier_asset_id: UUID
    """
    The underlier asset_id for this yield surface.
    """

    as_of_times: List[datetime]
    """
    Series of timestamps corresponding to the start of each yield surfaces.
    """

    projection_rates: Dict[str, List[NumberOrNone]]
    """
    The projection rates keyed by CTM projection rates (1D, 1W, 2W, 1M, 3M, 6M, 9M, 1Y).
    """
