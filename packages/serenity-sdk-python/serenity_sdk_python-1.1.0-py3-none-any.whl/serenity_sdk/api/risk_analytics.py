import json
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from serenity_sdk.api.core import CallType, SerenityApi, SerenityClient
from serenity_types.risk.simulators.greek_measures import GreekMeasureRequest, GreekMeasureResponse
from serenity_types.portfolio.core import Balance
from serenity_types.utils.common import Response
from serenity_types.valuation.portfolio_analytic import (
    BrinsonAttributionOutput,
    BrinsonAttributionRequest,
    PortfolioAnalyticOutput,
    PortfolioAnalyticRequest
)


class RiskAnalyticsAPI(SerenityApi):
    """
    Helper class for the Risk Analytics API.
    """

    def __init__(self, client: SerenityClient):
        """
        :param client: the raw client to delegate to when making API calls
        """

        # NOTE: I don't think the base endpoint should be valuation in the future but
        # understand this is the most practical arrangement to start; however, the
        # SDK client at least should be independent from valuation.
        super().__init__(client, "risk/analytics")

    def compute_portfolio_statistics(
        self, request: PortfolioAnalyticRequest
    ) -> Response[PortfolioAnalyticOutput]:
        """
        Given a rich portfolio object with periodic positions, trades and transfers,
        computes standard portfolio analytics like Sharpe, Sortino, max drawdown, etc..
        Optionally you can also include a set of "simulated trades" so you can see
        how portfolio performance would differ if you execute those trades, essentially
        perform a what-if analysis on past trading decisions or alternative portfolios.
        """
        req_json = json.loads(request.json(exclude_unset=True, by_alias=True))
        raw_json = self._call_api(
            api_path="/portfolio/valuation/compute",
            body_json=req_json,
            call_type=CallType.POST,
            api_version='v2'
        )
        return PortfolioAnalyticOutput.parse_obj(raw_json["result"])

    def compute_portfolio_performance_attribution(
        self, request: BrinsonAttributionRequest
    ) -> Response[BrinsonAttributionOutput]:
        """
        Given a rich portfolio object with periodic positions, trades and transfers,
        computes the Brinson performance attribution, assessing to what degree the
        performance is due to active management.
        """
        req_json = json.loads(request.json(exclude_unset=True, by_alias=True))
        raw_json = self._call_api(
            api_path="/brinson_attribution/compute",
            body_json=req_json,
            call_type=CallType.POST,
            api_version='v2'
        )
        return BrinsonAttributionOutput.parse_obj(raw_json["result"])

    def compute_greek_measures(
            self,
            as_of_time: Optional[datetime] = None,
            pf_as_of_time: Optional[datetime] = None,
            pf_metadata_id: Optional[UUID] = None,
            pf_balances: Optional[List[Balance]] = None,
            simulation_id: Optional[UUID] = None) -> GreekMeasureResponse:
        """
        Calculate the greek measures of the given portfolio balances.
        """
        if (pf_balances and pf_metadata_id) or (pf_balances is None and pf_metadata_id is None):
            raise ValueError("Please specify one of 'pf_metadata_id' or 'pf_balances'")
        body = GreekMeasureRequest(
            as_of_time=as_of_time,
            portfolio_as_of_time=pf_as_of_time,
            portfolio_metadata_id=pf_metadata_id,
            portfolio_balances=pf_balances,
            simulation_id=simulation_id
        )
        raw_json = self._call_api(
            api_path="/greek_measures/compute",
            body_json=json.loads(body.json()),
            call_type=CallType.POST,
            api_version='v2'
        )
        return GreekMeasureResponse.parse_obj(raw_json["result"])
