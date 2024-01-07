"""
Entity holders are used to store the simulator entities in flat dictionaries.
"""

from typing import Dict, Union
from pydantic import Field

from serenity_types.risk.simulators.driver_keys import DriverKey, DriverKeyId
from serenity_types.risk.simulators.simulator_contributors import (
    ContributorId,
    CustodyProviderContributor,
    CustodyTypeContributor,
    DriverKeyContributor,
    ModelFactorContributor,
    MoneynessContributor,
    QuotedAssetContributor,
    ResidualContributor,
    SimulatorRootContributor,
    SourcedPositionContributor,
    TenorContributor,
    UnderlierContributor,
)
from serenity_types.risk.simulators.simulator_trees import EntityTreeNode
from serenity_types.utils.serialization import CamelModel


class EntityHolder(CamelModel):
    """
    Holding all relevant simulation entities in a single place.
    """

    contributors: Dict[
        ContributorId,
        Union[
            CustodyProviderContributor,
            CustodyTypeContributor,
            DriverKeyContributor,
            MoneynessContributor,
            ModelFactorContributor,
            QuotedAssetContributor,
            SimulatorRootContributor,
            SourcedPositionContributor,
            TenorContributor,
            UnderlierContributor,
            ResidualContributor,
        ],
    ] = Field(default_factory=dict)
    """
    The flat dictionary of all contributors.
    """

    contributor_trees: Dict[str, EntityTreeNode] = Field(default_factory=dict)
    """
    The dictionary of all contributor trees. Note that the root node is enough to specify the whole tree.
    """

    driver_keys: Dict[DriverKeyId, DriverKey] = Field(default_factory=dict)
    """
    The dictionary of all driver keys.
    This field is empty if the simulation does not expose any driver entities.
    """
