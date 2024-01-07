"""
This module defines the types used by the simulator for Greek measures in financial computations.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import Field, root_validator
from serenity_types.counterparty.custody import CustodySource
from serenity_types.portfolio.core import Balance
from serenity_types.risk.simulators.entity_holders import EntityHolder
from serenity_types.risk.simulators.simulator_contributors import ContributorId
from serenity_types.utils.serialization import CamelModel


class GreekMeasureType(Enum):
    """
    Enumeration for different types of Greek measures.
    """

    VALUE = "Value"
    """
    The value zero-order mathematical derivative, i.e. the derivative-asset value itself.
    """

    DELTA = "Delta"
    """
    The delta's sensitivity to spot changes.
    """

    GAMMA = "Gamma"
    """
    The gamma's sensitivity to spot changes.
    """

    VEGA = "Vega"
    """
    The vega's sensitivity to volatility changes.
    """

    RHO = "Rho"
    """
    The rho's sensitivity to interest-rate changes.
    """

    THETA = "Theta"
    """
    The theta's sensitivity to time changes.
    """


class GreekMeasureReference(Enum):
    """
    Defines the reference context for Greek measures, like native, quantity, or currency.
    """

    NATIVE = "Native"
    """
    The Greek measure is related to the native pricing variable.
    This is the pure unalterated mathematical derivative value.
    """

    QUANTITY = "Quantity"
    """
    The Greek measure is related to the quantity of the instrument.
    """

    CURRENCY = "Currency"
    """
    The Greek measure is related to the currency of the instrument.
    """


class GreekMeasureAggregationType(Enum):
    """
    Specifies how Greek measures are aggregated, such as net, gross, or none.
    """

    NET = "Net"
    """
    The Greek measure is aggregated as is, i.e. keeping its sign.
    """

    GROSS = "Gross"
    """
    The absolute value of the Greek measure is aggregated, so that we always get a positive number.
    """

    NONE = "None"
    """
    No aggregation is performed on the Greek measure.
    """


class GreekMeasureUnit(Enum):
    """
    Units for representing Greek measures, like unity, percent, basis point, or day.
    """

    UNITY = "Unity"
    """
    The pure derivative value.
    """

    PERCENT = "Percent"
    """
    The percentage is Decimal("0.01").
    """

    BASIS_POINT = "BasisPoint"
    """
    The basis point is Decimal("0.0001").
    """

    DAY = "Day"
    """
    The day as a fraction of a year: Decimal("1")/Decimal("365").
    """


class GreekMeasureParameters(CamelModel):
    """
    Represents the parameters associated with a specific Greek measure.
    """

    tag: str = Field(..., allow_mutation=False)
    """
    The Greek measure unique identifier, unique within the list of Greek measures.
    This field is usially deterministically generated from the other fields.
    """

    measure_type: GreekMeasureType = Field(..., allow_mutation=False)
    """
    The risk-measure type chosen from the list of risk measure types.
    """

    reference: GreekMeasureReference = Field(..., allow_mutation=False)
    """
    The reference for the Greek measure.
    """

    aggregation_type: GreekMeasureAggregationType = Field(..., allow_mutation=False)
    """
    The aggregation type for the Greek measure.
    """

    unit: GreekMeasureUnit = Field(..., allow_mutation=False)
    """
    The Greek measure unit.
    """

    class Config:
        """
        Pydantic configuration class: we vaildate the assignments so that the fields cannot be changed after creation.
        """

        validate_assignment = True


class GreekMeasureRequest(CamelModel):
    """
    Represents the request for Greek-measure computation.
    Specify either portfolio_metadata_id or the full portfolio_balances by values.
    """

    as_of_time: Optional[datetime] = None
    """
    The as-of time to be used when askingb the data source for market data.
    If this is not specified, the latest market data will be used.
    """

    portfolio_as_of_time: Optional[datetime] = None
    """
    The as-of time used to determine which portfolio snapshot is to be used.
    Defaults to the value of the `as_of_time` parameter.
    """

    portfolio_metadata_id: Optional[UUID] = None
    """
    Portfolio metadata ID used to retrieve the balances if parameter `portfolio_balances` is not specified.
    """

    portfolio_balances: Optional[List[Balance]] = None
    """
    The balances by values, i.e. the list of positions to be used in the computation.
    If this is not specified, the balances will be retrieved from the database using the `portfolio_metadata_id`.
    """

    simulation_id: Optional[UUID] = None
    """
    Used to create a seed for the deterministic creation of the contributors ids.
    It can be used in future requests to obtain the same contributors ids, if the tree structure is the same.
    If this is not specified, a new simulation id will be created.
    """

    @root_validator
    def check_portfolio_snapshot_id_and_portfolio_balances(cls, values):
        if (values.get('portfolio_metadata_id') is None and values.get('portfolio_balances') is None) or \
                (values.get('portfolio_metadata_id') and values.get('portfolio_balances')):
            raise ValueError("Only one of 'portfolio_metadata_id' or 'portfolio_balances' should be specified.")
        return values


class InternalGreekMeasureRequest(CamelModel):
    """
    INTERNAL USE ONLY: for clients' risk services to call core risk services.
    """

    as_of_time: Optional[datetime] = None
    """
    The as-of time to use for loading all marketdata, surfaces, yield curves and refdata from the database.
    Defaults to the latest up to this time.
    """

    portfolio_balances: List[Balance]
    """
    The full portfolio balances by values.
    """

    custody_sources: List[CustodySource]
    """
    List of custody sources for the specified balances' accounts.
    """

    simulation_id: Optional[UUID] = None
    """
    Note that the `simulation_id` is optional. If it is not provided, a new one will be created.
    The `simulation_id` is used to create a seed for the deterministic creation contributors id's.
    It can be used in future requests to obtain the same contributors ids, if the tree structure is the same.
    """


class GreekMeasureResponse(CamelModel):
    """
    Results for the Greek measures.
    """

    as_of_time: datetime
    """
    The actual as_of_time used for the computation.
    """

    simulation_id: UUID
    """
    This actual simulation_id used to create the contributors ids.
    """

    balances: List[Balance]
    """
    The actual portfolio balances used for the computation.
    They might be different from the requested balances if there were duplications or null balances.
    """

    custody_sources: List[CustodySource]
    """
    The list of custody sources used in the computation.
    """

    greek_measure_parameters: Dict[str, GreekMeasureParameters]
    """
    A dictionary mapping Greek-measure tags to their corresponding parameters.
    Each tag represents a specific Greek measure (e.g., delta, gamma) with the associated calculation parameters.
    """

    entity_holder: EntityHolder
    """
    Encapsulates the information about the entities (such as financial instruments or portfolios)
    involved in the computation of Greek measures.
    """

    greek_measures: Dict[ContributorId, Dict[str, float]]
    """
    A nested dictionary where each key is a Contributor ID and its value is another dictionary mapping
    Greek-measure tags to their calculated values.
    This structure provides the computed Greek measures for each contributing entity.
    """

    intermediate_values: Dict[ContributorId, Dict[str, float]]
    """
    Contains intermediate computational variables, organized by Contributor ID.
    Each entry is a dictionary mapping variable tags to their respective values,
    providing insights into the calculations performed for each contributor.
    Not all contributors may have corresponding entries in this dictionary.
    """
