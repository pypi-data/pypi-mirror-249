from typing import Dict, Tuple, List
import pandas as pd
from serenity_sdk.api.provider import SerenityApiProvider
from serenity_types.pricing.derivatives.options.valuation import (
    OptionValuation,
    OptionValuationRequest)

from .table_plot import OptionValuationResultTablePlot
from .converters import convert_object_dict_to_df

import logging
logging = logging.getLogger(__name__)


def run_compute_option_valuations(
        api: SerenityApiProvider,
        the_optvals=Dict[str, OptionValuation],
        **kwargs) -> pd.DataFrame:
    """
    Function to run 'compute_option_valuation' and create results in dictionary format.

    :param api: Serenity Api provider
    :param the_optvals: dictionary of option valuations, defaults to Dict[str, OptionValuation]
    :return: dictionary of option valuation results
    """
    optval_keys, optval_requests = zip(*[[k, v] for k, v in the_optvals.items()])
    request = OptionValuationRequest(options=[v for v in optval_requests], **kwargs)
    val_results = api.pricer().compute_option_valuations(request)
    # use a helper object for output formatting
    ovr_tp = OptionValuationResultTablePlot(val_results, optval_keys)
    return ovr_tp.results_table


def run_multiple_option_valuation_requests(
        api: SerenityApiProvider,
        requests: Dict[str, OptionValuationRequest])\
        -> Tuple[pd.DataFrame, List[str], List[str]]:

    results = {}
    succeded = []
    failed = []
    for k, r in requests.items():
        try:
            if len(r.options) != 1:
                raise ValueError(f"Each valuation request must have exactly one option valuation. \
                    Please, check {k}.")
            results[k] = api.pricer().compute_option_valuations(r)
            succeded.append(k)
        except Exception:
            logging.warn(f"failed: {k}")
            failed.append(k)

    df = convert_object_dict_to_df({k: v[0] for k, v in results.items()})
    return df, succeded, failed
