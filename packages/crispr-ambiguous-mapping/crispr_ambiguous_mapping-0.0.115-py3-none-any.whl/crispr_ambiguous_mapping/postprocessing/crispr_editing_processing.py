from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Optional, DefaultDict, Union, Tuple
import pandas as pd
from typing import Counter as CounterType
from ..mapping.models import *

def check_match_result_non_error(match_result):
    return False if match_result is None else match_result.error is None # If match_result is None, treat as error. If match_result is not None, but error is None, then non_error

# Filter dict with observed sequence inference results for only those that do not contain any mapping errors
def get_non_error_dict(observed_guide_reporter_umi_counts_inferred, attribute_name):
    return {observed_guide_reporter_key: observed_guide_reporter_umi_counts_inferred_value for observed_guide_reporter_key, observed_guide_reporter_umi_counts_inferred_value in observed_guide_reporter_umi_counts_inferred.items() if check_match_result_non_error(getattr(observed_guide_reporter_umi_counts_inferred_value.inferred_value, attribute_name))}

def get_matchset_alleleseries(observed_guide_reporter_umi_counts_inferred: DefaultDict[Tuple[str,Optional[str],Optional[str]], dict], attribute_name: str, contains_umi: bool): 
    #
    #   DEFINE THE DEFAULTDICTS FOR COUNTING
    #
    ambiguous_ignored_umi_noncollapsed_alleledict : DefaultDict[Tuple[str, Optional[str], Optional[str]], DefaultDict[Tuple[str, Optional[str], Optional[str]], int]]  = defaultdict(lambda: defaultdict(int))
    ambiguous_ignored_umi_collapsed_alleledict : DefaultDict[Tuple[str, Optional[str], Optional[str]], DefaultDict[Tuple[str, Optional[str], Optional[str]], int]]  = defaultdict(lambda: defaultdict(int))
    ambiguous_ignored_alleledict : DefaultDict[Tuple[str, Optional[str], Optional[str]], DefaultDict[Tuple[str, Optional[str], Optional[str]], int]]  = defaultdict(lambda: defaultdict(int))

    ambiguous_accepted_umi_noncollapsed_alleledict : DefaultDict[Tuple[str, Optional[str], Optional[str]], DefaultDict[Tuple[str, Optional[str], Optional[str]], int]]  = defaultdict(lambda: defaultdict(int))
    ambiguous_accepted_umi_collapsed_alleledict : DefaultDict[Tuple[str, Optional[str], Optional[str]], DefaultDict[Tuple[str, Optional[str], Optional[str]], int]]  = defaultdict(lambda: defaultdict(int))
    ambiguous_accepted_alleledict : DefaultDict[Tuple[str, Optional[str], Optional[str]], DefaultDict[Tuple[str, Optional[str], Optional[str]], int]]  = defaultdict(lambda: defaultdict(int))

    ambiguous_spread_umi_noncollapsed_alleledict : DefaultDict[Tuple[str, Optional[str], Optional[str]], DefaultDict[Tuple[str, Optional[str], Optional[str]], float]]  = defaultdict(lambda: defaultdict(int))
    ambiguous_spread_umi_collapsed_alleledict : DefaultDict[Tuple[str, Optional[str], Optional[str]], DefaultDict[Tuple[str, Optional[str], Optional[str]], float]]  = defaultdict(lambda: defaultdict(int))
    ambiguous_spread_alleledict : DefaultDict[Tuple[str, Optional[str], Optional[str]], DefaultDict[Tuple[str, Optional[str], Optional[str]], float]]  = defaultdict(lambda: defaultdict(int))

    #
    # ITERATE THROUGH THE NON-ERROR INFERRED RESULTS AND FILL THE COUNTS
    #
    for observed_sequence, inferred_value_results in get_non_error_dict(observed_guide_reporter_umi_counts_inferred, attribute_name).items():
        #
        #   Get the relevant attributes
        #
        observed_value_counts: Union[CounterType[Optional[str]], int] = inferred_value_results.observed_value
        inferred_value_result: CompleteInferenceMatchResult =  inferred_value_results.inferred_value 
            
        match_set_single_inference_match_result : Optional[MatchSetSingleInferenceMatchResult] = getattr(inferred_value_result, attribute_name)
        assert match_set_single_inference_match_result is not None, "match_set_single_inference_match_result should not be none since this is from the non error list. Developer error."

        matches: pd.DataFrame = match_set_single_inference_match_result.value.matches
        if not matches.empty:
            # ITERATE THROUGH MATCHE(S) TO PERFORM COUNTS
            for whitelist_reporter_series in matches.iterrows(): 
                # UMI-BASED COUNTING
                whitelist_sequence_index = tuple(whitelist_reporter_series[1])
                observed_sequence_index = tuple(observed_sequence)
                if contains_umi:
                    assert isinstance(observed_value_counts, Counter), f"For UMI, expecting observed value is a Counter, but type is {type(observed_value_counts)}"
                    ambiguous_accepted_umi_noncollapsed_alleledict[whitelist_sequence_index][observed_sequence_index] += sum(observed_value_counts.values())
                    ambiguous_accepted_umi_collapsed_alleledict[whitelist_sequence_index][observed_sequence_index] += len(observed_value_counts.values())

                    ambiguous_spread_umi_noncollapsed_alleledict[whitelist_sequence_index][observed_sequence_index] += sum(observed_value_counts.values()) / float(matches.shape[0])
                    ambiguous_spread_umi_collapsed_alleledict[whitelist_sequence_index][observed_sequence_index] += len(observed_value_counts.values()) / float(matches.shape[0])
                    
                    # If there is no ambiguous matches, then add to ambiguous_ignored counter
                    if matches.shape[0] == 1:
                        ambiguous_ignored_umi_noncollapsed_alleledict[whitelist_sequence_index][observed_sequence_index] += sum(observed_value_counts.values())
                        ambiguous_ignored_umi_collapsed_alleledict[whitelist_sequence_index][observed_sequence_index] += len(observed_value_counts.values())

                # STANDARD NON-UMI BASED COUNTING
                else:
                    assert isinstance(observed_value_counts, int), f"For non UMI, expecting observed value is an int, but type is {type(observed_value_counts)}"
                    ambiguous_accepted_alleledict[whitelist_sequence_index][observed_sequence_index] += observed_value_counts
                    ambiguous_spread_alleledict[whitelist_sequence_index][observed_sequence_index] += observed_value_counts / float(matches.shape[0])

                    # If there is no ambiguous matches, then add to ambiguous_ignored counter
                    if matches.shape[0] == 1:
                        ambiguous_ignored_alleledict[whitelist_sequence_index][observed_sequence_index] += observed_value_counts

    # Helper function that converts defaultdict to series
    create_dict_counterseries = lambda alleledict : {whitelist_sequence_key: pd.Series(observed_sequence_counterdict) for whitelist_sequence_key, observed_sequence_counterdict in alleledict.items()}
    
    #
    #   CONVERT THE COUNT DICTS INTO PANDAS SERIES, since this is a more ideal structure.
    #
    match_set_whitelist_reporter_observed_sequence_counter_series_results = MatchSetWhitelistReporterObservedSequenceCounterSeriesResults()
    match_set_whitelist_reporter_observed_sequence_counter_series_results.ambiguous_ignored_umi_noncollapsed_alleleseries = create_dict_counterseries(ambiguous_ignored_umi_noncollapsed_alleledict)
    match_set_whitelist_reporter_observed_sequence_counter_series_results.ambiguous_ignored_umi_collapsed_alleleseries = create_dict_counterseries(ambiguous_ignored_umi_collapsed_alleledict)
    match_set_whitelist_reporter_observed_sequence_counter_series_results.ambiguous_ignored_alleleseries = create_dict_counterseries(ambiguous_ignored_alleledict)

    match_set_whitelist_reporter_observed_sequence_counter_series_results.ambiguous_accepted_umi_noncollapsed_alleleseries = create_dict_counterseries(ambiguous_accepted_umi_noncollapsed_alleledict)
    match_set_whitelist_reporter_observed_sequence_counter_series_results.ambiguous_accepted_umi_collapsed_alleleseries = create_dict_counterseries(ambiguous_accepted_umi_collapsed_alleledict)
    match_set_whitelist_reporter_observed_sequence_counter_series_results.ambiguous_accepted_alleleseries = create_dict_counterseries(ambiguous_accepted_alleledict)

    match_set_whitelist_reporter_observed_sequence_counter_series_results.ambiguous_spread_umi_noncollapsed_alleleseries = create_dict_counterseries(ambiguous_spread_umi_noncollapsed_alleledict)
    match_set_whitelist_reporter_observed_sequence_counter_series_results.ambiguous_spread_umi_collapsed_alleleseries = create_dict_counterseries(ambiguous_spread_umi_collapsed_alleledict)
    match_set_whitelist_reporter_observed_sequence_counter_series_results.ambiguous_spread_alleleseries = create_dict_counterseries(ambiguous_spread_alleledict)

    return match_set_whitelist_reporter_observed_sequence_counter_series_results

