"""
This module contains the types, enumerations and classes that represent the driver keys.

We use the generic term driver, instead of the more popular term risk driver, because the drivers described here
are not necessarily related to risk, as the could also be used for stress testing or sensitivity analysis.
"""

from enum import Enum
from typing import Tuple
from uuid import UUID

from pydantic import Field
from serenity_types.risk.simulators.entities import EntityId
from serenity_types.utils.serialization import CamelModel


class DriverKeyId(EntityId):
    """
    A unique identifier for all driver keys, currently an entity id.
    """


class DriverKeyType(Enum):
    """
    The enumeration of all possible driver-key types.

    Note that the representation string matches the corresponding model name (see below).
    """

    INTEREST_RATE = "InterestRateKey"
    """
    The interest-rate driver keys
    """
    EXCHANGE_RATE = "ExchangeRateKey"
    """
    The exchange-rate driver keys
    """
    SPOT_PRICE = "SpotPriceKey"
    """
    The spot-price driver keys
    """
    FUTURES_BASIS = "FuturesBasisKey"
    """
    The futures-basis driver keys
    """
    PERPETUAL_BASIS = "PerpetualBasisKey"
    """
    The perpetual-basis driver keys
    """
    PROJECTION_CURVE = "ProjectionCurveKey"
    """
    The projection-curve driver keys
    """
    PROJECTION_RATE = "ProjectionRateKey"
    """
    The projection-rate driver keys
    """
    VOLATILITY_SURFACE = "VolatilitySurfaceKey"
    """
    The volatility-surface driver keys
    """
    VOLATILITY_SLICE = "VolatilitySliceKey"
    """
    The volatility-slice driver keys
    """
    VOLATILITY_POINT = "VolatilityPointKey"
    """
    The volatility-point driver keys
    """


class DriverTenor(str):
    """
    The tenor of a driver such as a projection rate or a volatility point.

    Currently it is just a string, however we might add some verification logic in the future.
    """


class DriverMoneyness(str):
    """
    The moneyness of a driver, typically an implied volatility.

    Currently it is just a string, however we might add some verification logic in the future.
    """


class DriverKey(CamelModel):
    """
    The common attributes to all driver keys.
    """

    key_id: DriverKeyId = Field(..., allow_mutation=False)
    """
    A unique identifier for the risk driver key.
    This field should be a readable deterministic unique identifier, computed from the other fields.
    """
    description: str = Field(..., allow_mutation=False)
    """
    A summary of all the driver fields that can also be used as long unique identifier for the driver key itself.
    """
    driver_key_type: DriverKeyType = Field(..., allow_mutation=False)
    """
    The driver-key type, one of the values of the DriverKeyType enumeration.
    """

    class Config:
        """
        Pydantic configuration class: we vaildate the assignments so that the fields cannot be changed after creation.
        """

        validate_assignment = True


class InterestRateKey(DriverKey):
    """
    The interest rate of a currency at a given tenor
    """

    base_exposure_id: UUID = Field(..., allow_mutation=False)
    """
    The base exposure of the interest rate
    """
    tenor: DriverTenor = Field(..., allow_mutation=False)
    """
    The tenor of the interest rate
    """


# Exchange rate keys
class ExchangeRateKey(DriverKey):
    """
    The exchange rate between a base exposure and a quote exposure.
    This is the exchange rate is the base class for all keys that represent exchange rates.
    (This includes spot prices, which are exchange rates between an asset and a currency.)
    """

    base_exposure_id: UUID = Field(..., allow_mutation=False)
    """
    The base exposure of the exchange rate. E.g., the UUID of BTC in a BTC/USD exchange rate
    """
    quote_exposure_id: UUID = Field(..., allow_mutation=False)
    """
    The quote exposure of the exchange rate. E.g., the UUID of USD in a BTC/USD exchange rate
    """


class SpotPriceKey(ExchangeRateKey):
    """
    The spot price of an asset in the quoted exposure.
    In a BTC/USD spot price, the base exposure is BTC and the quote exposure is USD.
    """


class FuturesBasisKey(ExchangeRateKey):
    """
    The basis of futures contracts.
    """


class PerpetualBasisKey(ExchangeRateKey):
    """
    The basis of perpetual contracts.
    """


# Term structure keys.
# A term structure is a driver that can be seen as a function of a maturity


class ProjectionRateKey(ExchangeRateKey):
    """
    The projection rate of an asset with respect to a currency
    """

    tenor: DriverTenor = Field(..., allow_mutation=False)
    """
    The tenor of the projection rate
    """


class ProjectionCurveKey(ExchangeRateKey):
    """
    The entire projection curve composed of many projection rates.
    """

    rates: Tuple[DriverKeyId, ...] = Field(..., allow_mutation=False)
    """
    The list of ids of the projection rates that compose the projection curve
    """


# Volatility keys, used for implied volatilities.


class VolatilityPointKey(ExchangeRateKey):
    """
    A single volatility point.
    The implied volatility of an asset with respect to a currency at a given tenor and moneyness.
    """

    tenor: str = Field(..., allow_mutation=False)
    """
    The volatility tenor.
    """
    moneynesses: DriverMoneyness = Field(..., allow_mutation=False)
    """
    The volatility moneyness.
    """


class VolatilitySliceKey(ExchangeRateKey):
    """
    A slice of the volatility surface, i.e. a reference to all volatility points with the same tenor.
    """

    tenor: DriverTenor = Field(..., allow_mutation=False)
    """
    The volatility tenor.
    """
    points: Tuple[DriverKeyId, ...] = Field(..., allow_mutation=False)
    """
    The list of ids of the volatility points that compose the volatility slice.
    """


class VolatilitySurfaceKey(ExchangeRateKey):
    """
    The entire volatility surface composed of many volatility slices.
    """

    slices: Tuple[DriverKeyId, ...] = Field(..., allow_mutation=False)
    """
    The list of ids of the volatility slices that compose the volatility surface.
    """
