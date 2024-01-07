"""
Simulator contributors specify elements to which we can associate a measure contribution.
"""

from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import Field
from serenity_types.counterparty.custody import CustodyProviderType
from serenity_types.risk.measures import OTCAssetTypes
from serenity_types.risk.simulators.driver_keys import (
    DriverKey,
    DriverMoneyness,
    DriverTenor,
)
from serenity_types.risk.simulators.entities import EntityId
from serenity_types.utils.serialization import CamelModel


class ContributorId(EntityId):
    """
    A unique identifier for the simulator contributors.
    It is currently just an entity id.
    """


class ContributorType(Enum):
    """
    The enumeration of all simulator contributor types.
    Note that the representation string matches the corresponding model name (see below).
    """

    PORTFOLIO_SNAPSHOT = "PortfolioSnapshotContributor"
    """
    The simulator contributor is a portfolio snapshot.
    """

    SIMULATOR_ROOT = "SimulatorRootContributor"
    """
    The simulator contributor is a root node.
    """

    QUOTED_ASSET = "QuotedAssetContributor"
    """
    The simulator contributor is a quoted asset.
    """

    OTC_ASSET = "OtcAssetContributor"
    """
    The simulator contributor is an OTC asset.
    """

    MODEL_FACTOR = "ModelFactorContributor"
    """
    The simulator contributor is a model factor.
    """

    DRIVER_KEY = "DriverKeyContributor"
    """
    The simulator contributor is a driver key.
    """

    RESIDUAL = "ResidualContributor"
    """
    The simulator contributor is a residual value.
    """

    TENOR = "TenorContributor"
    """
    The simulator contributor holds contributor values with the same tenor.
    """

    MONEYNESS = "MoneynessContributor"
    """
    The simulator contributor holds contributor values with the same moneyness.
    """

    CUSTODY_PROVIDER = "CustodyProviderContributor"
    """
    The custodian contributor holds contributor values for the same custodian.
    """

    CUSTODY_TYPE = "CustodyTypeContributor"
    """
    The custody-type contributor holds contributor values for the same custody type.
    """

    UNDERLIER = "UnderlierContributor"
    """
    The underlier contributor holds contributor values for the same underlier.
    """

    SOURCED_POSITION = "SourcedPositionContributor"
    """
    The balance contributor of an asset in an account.
    """

    UNSOURCED_POSITION = "UnsourcedPositionContributor"
    """
    The balance contributor of an asset that is not in an account.
    """


class SimulatorContributor(CamelModel):
    """
    The base model for all simulator contributors.
    """

    contributor_id: ContributorId = Field(..., allow_mutation=False)
    """
    A readable deterministic unique identifier for the simulator contributor.
    This field should be computed by a factory from the other fields after the object creation.
    """
    description: str = Field(..., allow_mutation=False)
    """
    A summary of all the contributor fields that can also be used as long unique identifier this contributor.
    This should be computed by a factory deterministically from the other fields.
    """
    contributor_type: ContributorType = Field(..., allow_mutation=False)
    """
    The type of the simulator contributor.
    """

    class Config:
        """
        Pydantic configuration: we vaildate the assignments so that the fields cannot be changed after creation.
        """

        validate_assignment = True


# Root contributors


class PortfolioSnapshotContributor(SimulatorContributor):
    """
    The simulator contributor for portfolio snapshots.
    Usually, there is only one portfolio snapshot per simulation.
    Note that this contributor cannot be a child of any other contributor.
    """

    snapshot_id: UUID = Field(..., allow_mutation=False)
    """
    The unique identifier of the portfolio snapshot
    """

    description: str = Field(..., allow_mutation=False)
    """
    A unique description of the portfolio-snapshot contributor.
    It can be used to create different tree roots for the same portfolio snapshot.
    """


class SimulatorRootContributor(SimulatorContributor):
    """
    The simulator contributor for root nodes.
    There might be multiple root nodes per simulation, these are distinguished by the description field.
    Note that this contributor cannot be a child of any other contributor.
    """

    simulation_id: UUID = Field(..., allow_mutation=False)
    """
    Used to create a seed for the deterministic creation of the contributors ids.
    It can be used in future requests to obtain the same contributors ids, if the tree structure is the same.
    """

    description: str = Field(..., allow_mutation=False)
    """
    A unique description of the root node contributor.
    It can be used to create different tree roots for the same simulation id.
    """


# Contributors that refer to other contributors (i.e. non-root contributors)


class ChildContributor(SimulatorContributor):
    """
    A child contributor always has a parent contributor as a reference.
    This is a base class and should not be instantiated directly, however this is not enforced in the code.
    """

    parent_id: ContributorId = Field(..., allow_mutation=False)
    """
    The contributor id to which this child contribution referes to.
    """


class QuotedAssetContributor(ChildContributor):
    """
    The simulator contributor for quoted assets.
    There should be one, and only one, quoted asset contributor for each quoted asset.
    """

    asset_id: UUID = Field(..., allow_mutation=False)
    """
    The unique identifier of the quoted asset
    """


class OtcAssetContributor(ChildContributor):
    """
    The simulator contributor for OTC assets
    """

    # TODO: since different users may use the same identifier for different OTC assets;
    # TODO: do we need a user identofier as well?
    otc_asset_id: str = Field(..., allow_mutation=False)
    """
    User specified unique identifier of the OTC asset.
    """
    otc_asset_type: OTCAssetTypes = Field(..., allow_mutation=False)
    """
    Serenity classification of OTC assets
    """


class ModelFactorContributor(ChildContributor):
    """
    The simulator contributor for model factors.
    The model-factor contributor usually referes to a portfolio snapshot, a quoted asset or an OTC asset.
    """

    model_config_id: UUID = Field(..., allow_mutation=False)
    """
    The unique identifier of the factor model
    """
    factor_name: str = Field(..., allow_mutation=False)
    """
    The name of the factor in the factor model specified by the model_config_id.
    E.g. 'momentum' or 'size'"
    """


class ResidualContributor(ChildContributor):
    """
    The residual contributor for another contributor.
    As sometimes the sum of the standard contributors is not equal to the total, we need for add a residual contributor.
    The reference contributor is usually a portfolio snapshot, a quoted asset or an OTC asset.
    """


class DriverKeyContributor(ChildContributor):
    """
    The simulator contributor for a driver key.

    For example, contributor by the volatility related to the portfolio-snapshot.
    """

    driver_key: DriverKey = Field(..., allow_mutation=False)
    """
    A copy of the driver key associated with this contributor.
    """


class TenorContributor(ChildContributor):
    """
    The simulator contributor for a tenor related for another contributor.

    For example, the contributor of the 3-month projection rate related for a portfolio-snapshot contributor.
    """

    tenor: DriverTenor = Field(..., allow_mutation=False)
    """
    The tenor of this contributor.
    """


class MoneynessContributor(ChildContributor):
    """
    The simulator contributor for the moneyness.

    For example, the contributor of the 50-sigma volatility related for a portfolio-snapshot contributor.
    """

    moneyness: DriverMoneyness = Field(..., allow_mutation=False)
    """
    The moneyness of this contributor
    """


# Contibutors specific to concentration risk


class CustodyProviderContributor(ChildContributor):
    """
    The simulator contributor for a custody provider.
    For example the ID of a certified custodian.
    """

    provider_id: Optional[UUID] = Field(..., allow_mutation=False)
    """
    The ID of the custody provider.
    """


class CustodyTypeContributor(ChildContributor):
    """
    The simulator contributor for a custody type.
    For example, a cold wallet, a centralized exchange, a certified custodian, and so on.
    """

    custody_provider_type: CustodyProviderType = Field(..., allow_mutation=False)
    """
    The unique identifier of the custody type
    """


class UnderlierContributor(ChildContributor):
    """
    The simulator contributor for an underlier.
    For example, the contributor that gathers together all derivative with a specific underlying asset.
    """

    asset_id: UUID = Field(..., allow_mutation=False)
    """
    The unique identifier of the underlier.
    Note that in the future we might also allow a tuple of UUID, to represent no underlier or a multiplicity of them.
    """


class SourcedPositionContributor(ChildContributor):
    """
    The simulator contributor for a balance that has an account id.
    Since these contributors are uniquely identified by the asset_id and the account_id,
    balances with the same asset_id and account_id are grouped together.
    """

    asset_id: UUID = Field(..., allow_mutation=False)
    """
    The unique asset identifier.
    """

    account_id: UUID
    """
    Unique identifier of the account for transaction information.
    """


class UnsourcedPositionContributor(ChildContributor):
    """
    The simulator contributor for a balance that has the asset id only.
    Since these contributors are uniquely identified by the asset_id, balances with the same asset_id
    are grouped together.
    """

    asset_id: UUID = Field(..., allow_mutation=False)
    """
    The unique asset identifier.
    """
