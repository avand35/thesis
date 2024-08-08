import pandas as pd
import numpy as np
import re
import math
import pandasql as ps
import time
import string
from typing import Any, Callable
import copy
# from relative_entropy import 


def convert_to_array(to_convert, cast_to_float = False) -> np.array:
    if isinstance(to_convert, list):
        if cast_to_float:
            return np.array([float(item) for item in to_convert])
        else:
            return np.array(to_convert)
    
    if math.isnan(to_convert):
        return np.asarray([])

    if '"' in to_convert:
        inside_value = False
        result = []
        current_string = ""

        for char in to_convert:
            if char == '"':
                if not inside_value:
                    inside_value = True
                elif inside_value:
                    inside_value = False  
            elif char == ',' and not inside_value:
                result.append(current_string.strip())
                current_string = ""
            elif inside_value:
                current_string += char

        if current_string:
            result.append(current_string.strip())

        return np.array(result)
    else:
        clean_string = to_convert.replace("{","").replace("}","")
        if not cast_to_float:
            return np.asarray([item.strip() for item in clean_string.split(",")])
        else:
            return np.asarray([float(item.strip()) for item in clean_string.split(",")])

    
def get_stat(stats: pd.DataFrame, attname: str, statname: str) -> str:
    return stats[stats["attname"] == attname][statname].values[0]

def get_bucket_idx(histogram_bounds, val):
    for i, bound in enumerate(histogram_bounds[1:]):
        if val < bound:
            return i
    return -1

class DB_stats:

    attname: str
    n_distinct: int 
    most_common_vals: np.array
    most_common_freqs: np.array
    histogram_bounds: np.array
    dist: pd.Series

    unmsk_n_distinct: int
    unmsk_most_common_vals: np.array
    unmsk_most_common_freqs: np.array
    unmsk_histogram_bounds: np.array
    unmsk_dist: pd.Series

    def __init__(self, stats: pd.DataFrame, attname: str):
        self.attname = attname
        self.n_distinct = get_stat(stats, attname, "n_distinct")
        self.most_common_vals = convert_to_array(get_stat(stats, attname, "most_common_vals"))
        self.most_common_freqs = convert_to_array(get_stat(stats, attname, "most_common_freqs"), True)
        self.histogram_bounds = convert_to_array(get_stat(stats, attname, "histogram_bounds"))
        self.dist = pd.Series(self.most_common_freqs, index = self.most_common_vals)

        self.unmsk_dist = None
        self.hist_apprx_freq = None

    def perturbation(self):
        self.unmsk_dist = self.dist
        self.unmsk_most_common_vals = self.most_common_vals
        self.unmsk_most_common_freqs = self.most_common_freqs
        self.unmsk_n_distinct = self.n_distinct
        self.unmsk_histogram_bounds = self.histogram_bounds

    def inverse_dist(self, inverse_mf: Callable[[Any], list], generalization_degree = -1):
        new_vals = []
        new_freqs = []
        for msk_val in self.dist.index:
            unmsk_vals = inverse_mf(msk_val)
            new_vals.extend(unmsk_vals)
            new_freq = self.dist[msk_val] / len(unmsk_vals)
            new_freqs.extend([new_freq] * len(unmsk_vals))
        if generalization_degree < 1:
            self.generalization_degree = float(len(new_vals))/float(len(self.most_common_vals))
        else:
            self.generalization_degree = generalization_degree
        self.unmsk_dist = pd.Series(new_freqs, index = new_vals)
        self.unmsk_most_common_vals = np.asarray(new_vals)
        self.unmsk_most_common_freqs = np.asarray(new_freqs)
        self.unmsk_n_distinct = int(self.n_distinct * self.generalization_degree)



    def inverse_histogram_bounds(self, inverse_mf: Callable[[Any], list]):
        unmk_bounds = []
        hist_size = len(self.histogram_bounds)
        for i, bound in enumerate(self.histogram_bounds):
            unmk_vals = inverse_mf(bound)
            if i < hist_size-1:
                unmk_bounds.append(unmk_vals[0])
            else:
                unmk_bounds.append(unmk_vals[-1])
        self.unmsk_histogram_bounds = np.asarray(unmk_bounds)

    def get_bucket_idx(self, val):
        if self.alphabet is not None:
            if self.hist_idx is None:
                self.hist_idx = [self.alphabet.index(bound) for bound in self.histogram_bounds]
            alph_idx = self.alphabet.index(val)
            for i, bound in enumerate(self.hist_idx[1:]):
                if alph_idx < bound:
                    return i
                
        for i, bound in enumerate(self.histogram_bounds[1:]):
            if val < bound:
                return i
        return -1

    def get_unmsk_bucket_idx(self, val):
        if self.alphabet is not None:
            if self.hist_idx is None:
                self.hist_idx = [self.alphabet.index(bound) for bound in self.unmsk_histogram_bounds]
            alph_idx = self.alphabet.index(val)
            for i, bound in enumerate(self.hist_idx[1:]):
                if alph_idx < bound:
                    return i
        for i, bound in enumerate(self.unmsk_histogram_bounds[1:]):
            if val < bound:
                return i
        return -1

    def estimate_hist_freq(self, alphabet: list, masked: bool = False) -> np.array:
        if self.histogram_bounds.size == 0:
            return
        if not masked:
            histogram_bounds = self.histogram_bounds
            most_common_vals = self.most_common_vals
            remaining_n_distinct = self.n_distinct - self.most_common_vals.size
            hist_bin_freq = (1 - self.most_common_freqs.sum()) / (self.histogram_bounds.size - 1)
        else:
            histogram_bounds = self.unmsk_histogram_bounds
            most_common_vals = self.unmsk_most_common_vals
            remaining_n_distinct = self.unmsk_n_distinct - self.unmsk_most_common_vals.size
            hist_bin_freq = (1 - self.unmsk_most_common_freqs.sum()) / (self.unmsk_histogram_bounds.size - 1)

        self.alphabet = alphabet
        # Get number of possible distinct values in every bucket
        hist_idx = [alphabet.index(bound) for bound in histogram_bounds]
        hist_n_distinct = np.asarray([hist_idx[i+1] - hist_idx[i] for i in range(len(hist_idx)-1)])
        total_n_distinct_hist = hist_idx[-1] - hist_idx[0]

        self.hist_idx = hist_idx
        # Remove know values from each bucket
        for val in most_common_vals:
            if not masked:
                idx = self.get_bucket_idx(val)
            else: 
                idx = self.get_unmsk_bucket_idx(val)
            if idx >= 0:
                hist_n_distinct[idx] -= 1
        
        # compute relative amount of distinct values in each bucket w.r.t. the total 
        # number of distinct velues and then estimate amount of distinct values in each bucket
        hist_rel_n_distinct = hist_n_distinct / total_n_distinct_hist
        self.hist_apprx_n_distinct = hist_rel_n_distinct * remaining_n_distinct
        
        # compute the approximate frequency of each possible value in each bucket
        self.hist_apprx_freq = hist_bin_freq / self.hist_apprx_n_distinct

    def addapt_freq_selectivity(self, selectivity):
        assert(selectivity >= 0.0 and selectivity <= 1.0, "The selectivity needs to be a value between 0.0 and 1.0")
        if self.unmsk_dist is None:
            self.dist = self.dist * selectivity
            # if self.n_distinct != self.dist.size:
            #     self.n_distinct = (self.n_distinct - self.dist.size) * selectivity + self.dist.size
            self.dist.at["NaN"] = 1.0 - selectivity
        else:
            self.unmsk_dist = self.unmsk_dist * selectivity
            # if self.unmsk_n_distinct != self.unmsk_dist.size:
            #     self.unmsk_n_distinct = (self.unmsk_n_distinct - self.unmsk_dist.size) * selectivity + self.unmsk_dist.size
            self.unmsk_dist.at["NaN"] = 1.0 - selectivity

        if self.hist_apprx_freq is not None:
            self.hist_apprx_freq = self.hist_apprx_freq * selectivity
            # self.hist_apprx_n_distinct = self.hist_apprx_freq * selectivity

def estimate_rel_entropy(original_stats: DB_stats, masked_stats: DB_stats, selectivity_original = 1.0, selectivity_masked = 1.0):
    original_stats_copy = copy.deepcopy(original_stats)
    masked_stats_copy = copy.deepcopy(masked_stats)
    if selectivity_original != 1.0:
        original_stats_copy.addapt_freq_selectivity(selectivity_original)
    if selectivity_masked != 1.0:
        masked_stats_copy.addapt_freq_selectivity(selectivity_masked)
    
    return estimate_rel_entropy_no_ref(original_stats_copy, masked_stats_copy)

# estimate entropy without the equi depth histogram 
def estimate_rel_entropy_no_ref(original_stats: DB_stats, masked_stats: DB_stats):
    # values is the set of values in the alphabet
    values = original_stats.dist.index.union(masked_stats.unmsk_dist.index, sort=False)

    # compute entropy only considering real frequencies
    count = 0
    comulative_freq = 0.0
    relative_entropy = 0.0

    to_recompute = []
    to_add = []
    for x in values:
        p_x = 0.0
        try:
            p_x = original_stats.dist[x]
        except:
            p_x = 0.0
        
        q_x = 0.0
        try:
            q_x = masked_stats.unmsk_dist[x]
        except:
            q_x = 0.0
            
        if q_x == 0.0 and p_x > 0.0:
            # print(str(x)+" has a q probability of 0, and p_x "+str(p_x))
            to_recompute.append(x)

        # TODO: check impact on other parts
        if p_x == 0.0 and q_x > 0.0:
            count += 1
            comulative_freq += q_x
            to_add.append(x)
        
        if p_x > 0.0 and q_x > 0.0:
            relative_entropy += p_x*np.log2(p_x/q_x)

    # Equi-depth histograms available in both stats
    if original_stats.hist_apprx_freq is not None and masked_stats.hist_apprx_freq is not None:
        # add values from the masked distribution that were missing in the original into the equi-depth histogram
        for x in to_add:
            bin_idx = masked_stats.get_unmsk_bucket_idx(x)           
            freq_sum = (masked_stats.hist_apprx_freq[bin_idx] * masked_stats.hist_apprx_n_distinct[bin_idx]) + masked_stats.unmsk_dist[x]
            masked_stats.hist_apprx_n_distinct[bin_idx] += 1
            masked_stats.hist_apprx_freq[bin_idx] = freq_sum / (masked_stats.hist_apprx_n_distinct[bin_idx])
            
        # recompute entropy for missing values with exact frequency in the original stats and no entry in the masked stats
        for x in to_recompute:
            p_x = original_stats.dist[x]
            bin_idx = masked_stats.get_unmsk_bucket_idx(x)
            approx_q_x = masked_stats.hist_apprx_freq[bin_idx]
            relative_entropy += p_x*np.log2(p_x/approx_q_x)
        if original_stats.dist.sum() < 0.8:
            # compute entropy of elements with approximate frequencies
            for ogl_bin_idx, high_bin_bound in enumerate(original_stats.histogram_bounds[1:]):
                low_bin_bound = original_stats.histogram_bounds[ogl_bin_idx]
                approx_p_x = original_stats.hist_apprx_freq[ogl_bin_idx]

                msk_bin_idx_low = masked_stats.get_unmsk_bucket_idx(low_bin_bound)
                msk_bin_idx_high = masked_stats.get_unmsk_bucket_idx(high_bin_bound)

                # check if only one bin is required
                if msk_bin_idx_low == msk_bin_idx_high:
                    approx_q_x = masked_stats.hist_apprx_freq[msk_bin_idx_low]
                    relative_entropy += original_stats.hist_apprx_n_distinct[ogl_bin_idx] * (approx_p_x*np.log2(approx_p_x/approx_q_x))
                else:
                    possible_n_distinct = np.zeros(np.abs(msk_bin_idx_high + 1 - msk_bin_idx_low))
                    # compute number of possible values in first and last bin
                    possible_n_distinct[0] = original_stats.alphabet.index(masked_stats.unmsk_histogram_bounds[msk_bin_idx_low + 1]) - original_stats.alphabet.index(low_bin_bound)
                    possible_n_distinct[-1] = original_stats.alphabet.index(high_bin_bound) - original_stats.alphabet.index(masked_stats.unmsk_histogram_bounds[msk_bin_idx_high])
                    # compute number of possible values in middle bins
                    for i, idx in enumerate(range(msk_bin_idx_low + 1, msk_bin_idx_high)):
                        possible_n_distinct[i+1] = original_stats.alphabet.index(masked_stats.unmsk_histogram_bounds[idx + 1]) - original_stats.alphabet.index(masked_stats.unmsk_histogram_bounds[idx])
                    # compute relative portion of distinct values in each bin
                    rel_possible_n_distinct = possible_n_distinct / possible_n_distinct.sum()

                    for i, idx in enumerate(range(msk_bin_idx_low, msk_bin_idx_high + 1)):
                        approx_q_x = masked_stats.hist_apprx_freq[idx]
                        apprx_n_distinct_bin = rel_possible_n_distinct[i] * original_stats.hist_apprx_n_distinct[ogl_bin_idx]
                        relative_entropy += apprx_n_distinct_bin * (approx_p_x*np.log2(approx_p_x/approx_q_x))

    # Equi-depth histogram available only for the original dataset
    elif original_stats.hist_apprx_freq is not None and masked_stats.hist_apprx_freq is None:
        # recompute entropy for missing values with exact frequency in the original stats and no entry in the masked stats
        masked_rest_freq = 1.0 - masked_stats.unmsk_dist.sum() + comulative_freq
        masked_n_appx_vals = masked_stats.unmsk_n_distinct - masked_stats.unmsk_dist.size + count
        masked_appx_freq = masked_rest_freq / masked_n_appx_vals
        
        for x in to_recompute:
            p_x = original_stats.dist[x]
            relative_entropy += p_x*np.log2(p_x/masked_appx_freq)
        
        if original_stats.dist.sum() < 0.8:
            # compute entropy of elements with approximate frequencies
            for ogl_bin_idx, approx_p_x in enumerate(original_stats.hist_apprx_freq):
                relative_entropy += original_stats.hist_apprx_n_distinct[ogl_bin_idx] * (approx_p_x*np.log2(approx_p_x/masked_appx_freq))

    else:        
        # recompute entropy for missing values with exact frequency in the original stats and no entry in the masked stats
        masked_rest_freq = 1.0 - masked_stats.unmsk_dist.sum() + comulative_freq
        masked_n_appx_vals = masked_stats.unmsk_n_distinct - masked_stats.unmsk_dist.size + count
        masked_appx_freq = masked_rest_freq / masked_n_appx_vals

        for x in to_recompute:
            p_x = original_stats.dist[x]
            relative_entropy += p_x*np.log2(p_x/masked_appx_freq)

        if original_stats.dist.sum() < 0.8:
            # compute entropy of elements with approximate frequencies
            original_rest_freq = 1.0 - original_stats.dist.sum()
            original_n_appx_vals = original_stats.n_distinct - original_stats.dist.size
            original_appx_freq = original_rest_freq / original_n_appx_vals

            if original_appx_freq > 0.0001 and masked_appx_freq > 0.0001:
                relative_entropy += original_n_appx_vals * (original_appx_freq*np.log2(original_appx_freq/masked_appx_freq))
    return relative_entropy