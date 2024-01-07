from enum import Enum
from uuid import UUID
from typing import Optional
from serenity_types.utils.serialization import CamelModel


class CustodyProviderType(Enum):
    """
    High-level classification of custody providers. This is the entry point for
    assessing counterparty risk: within each bucket there can be a finer-grained
    rating of the risk, so you can have a low- or high-risk exchange or smart
    contract and also distinguish between the risk of self-custody vs. custody
    at a qualified custodian at a higher level.
    """

    SELF_CUSTODY = 'SELF_CUSTODY'
    """
    A simple token balance in a wallet, possibly multi-sign like Gnosis Safe.
    """

    MANAGED_SELF_CUSTODY = 'MANAGED_SELF_CUSTODY'
    """
    A policy-managed MPC wallet, e.g. Fireblocks.
    """

    EXCHANGE_WALLET = 'EXCHANGE_WALLET'
    """
    An exchange hot wallet.
    """

    INSTITUTIONAL_CUSTODIAN = 'INSTITUTIONAL_CUSTODIAN'
    """
    An independent, institutional-grade custodian like Copper, but not a QC.
    """

    QUALIFIED_CUSTODIAN = 'QUALIFIED_CUSTODIAN'
    """
    A regulated qualified custodian, e.g. Standard Custody or BitGo.
    """

    SMART_CONTRACT_LOCK = 'SMART_CONTRACT_LOCK'
    """
    Balances locked / escrowed in a smart contract
    """

    MANUAL = 'MANUAL'
    """
    Manually created balances / positions.
    """


class CustodySource(CamelModel):
    """
    Represents a custody source for a counterparty.
    """
    custody_type: CustodyProviderType
    """
    The type of custody provider.
    """
    provider_id: Optional[UUID] = None
    """
    The ID of the custody provider.
    """
    connector_id: Optional[UUID] = None
    """
    The ID of the connector.
    """
    account_id: Optional[UUID] = None
    """
    The ID of the custody account.
    """
    provider_name: str
    """
    The name of the custody provider.
    """
    account_name: str
    """
    The name of the custody account.
    """
