import pandas as pd
import numpy as np
import re
import math
import pandasql as ps
import time
import string
from typing import Any, Callable
import copy

def disolve_tuples(x: tuple):
    if isinstance(x, tuple) and len(x) == 1:
        try:
            float(x[0])
            return float(x[0])
        except Exception:
            return x[0]
    else:
        return x

def relative_entropy(P_dist: pd.Series, Q_dist: pd.Series, table_size_q: int):
    # P and Q should have the values they represent in the index attribute
    P = P_dist.copy()
    Q = Q_dist.copy()

    P.index = P.index.map(disolve_tuples)
    Q.index = Q.index.map(disolve_tuples)


    # values is the set of values in the alphabet
    values = P.index.union(Q.index, sort=False)
    
    missing_values = []
    for x in values:
        p_x = 0.0
        try:
            p_x = P[x]
        except:
            p_x = 0.0
        
        q_x = 0.0
        try:
            q_x = Q[x]
        except:
            q_x = 0.0
        # Ensure absolute continuity
        if q_x == 0.0 and p_x > 0.0:
            missing_values.append(x)

    if len(missing_values) > 0:
        new_size = table_size_q + len(missing_values)
        for q_val in Q.index:
            old_prob = Q[q_val]
            freq = table_size_q*old_prob
            Q[q_val] = freq / new_size
        
        new_vals = pd.Series(data=[1/new_size]*len(missing_values), index=missing_values)
        Q = pd.concat([Q, new_vals])
    
        
    relative_entropy = 0.0
    for x in values:
        p_x = 0.0
        try:
            p_x = P[x]
        except:
            p_x = 0.0
        
        q_x = 0.0
        try:
            q_x = Q[x]
        except:
            q_x = 0.0

        if q_x == 0.0 and p_x > 0.0:
            raise ValueError("This should not happen...")

        if p_x > 0.0 and q_x > 0.0:
            relative_entropy += p_x*np.log2(p_x/q_x)
    # print(relative_entropy)
    return relative_entropy

def relative_entropy_suppressed(P_dist: pd.Series, table_size_p: int):
    n_distinct = len(P_dist)
    if n_distinct == table_size_p:
        # Only unique values
        p_x = 1.0 / table_size_p
        q_x = 1.0 / (table_size_p**2)
        relative_entropy = table_size_p * p_x*np.log2(p_x/q_x)
        print(relative_entropy)
        return relative_entropy
    else:
        relative_entropy = 0.0
        P = P_dist.copy()
        P.index = P.index.map(disolve_tuples)

        for x in P.index:
            p_x = P[x]
            q_x = 1.0 / (table_size_p*n_distinct)
            relative_entropy += p_x*np.log2(p_x/q_x)
        print(relative_entropy)
        return relative_entropy
    
def relative_entropy_generalization(P_dist: pd.Series, Q_dist: pd.Series, table_size_q: int, masking_function: Callable[[Any], Any], generalization_degree: int):
    # P and Q should have the values they represent in the index attribute
    P = P_dist.copy()
    Q = Q_dist.copy()

    P.index = P.index.map(disolve_tuples)
    Q.index = Q.index.map(disolve_tuples)

    missing_values = {}
    missing = 0.0
    for x in P.index:
        msk_val = masking_function(x)        
        q_x = 0.0
        try:
            q_x = Q[msk_val]
        except:
            # Ensure absolute continuity
            missing += 1.0
            if msk_val not in missing_values:
                missing_values[msk_val] = 1.0
            else:
                missing_values[msk_val] += 1.0

    if missing > 0:
        new_size = table_size_q + missing
        for q_val in Q.index:
            old_prob = Q[q_val]
            freq = table_size_q*old_prob
            Q[q_val] = freq / new_size
        for val in missing_values:
            missing_values[val] = missing_values[val] / new_size
        new_vals = pd.Series(val)
        Q = pd.concat([Q, new_vals])

    relative_entropy = 0.0
    for x in P.index:
        p_x = P[x]
        msk_val = masking_function(x)
        q_x = 0.0
        try:
            q_x = Q[msk_val] / generalization_degree
        except:
            q_x = 0.0
            
        if q_x == 0.0 or p_x == 0.0:
            relative_entropy += p_x*np.log2(generalization_degree)
        else:
            relative_entropy += p_x*np.log2(p_x/q_x)
    print(relative_entropy)   
    return relative_entropy


def relative_entropy_sel(P_dist: pd.Series, table_size_p: int, Q_dist: pd.Series, table_size_q: int):
    rel_entropy = relative_entropy(P_dist, Q_dist, table_size_q)
    penalty_factor = 1.0 + (np.abs(table_size_p - table_size_q) / table_size_p)
    return penalty_factor * rel_entropy

def relative_entropy_card(P_dist: pd.Series, table_size_p: int, Q_dist: pd.Series, table_size_q: int):
    # P and Q should have the values they represent in the index attribute
    P = P_dist.copy()
    Q = Q_dist.copy()

    P.index = P.index.map(disolve_tuples)
    Q.index = Q.index.map(disolve_tuples)


    card_diff = np.abs(table_size_p - table_size_q)    
    if table_size_p > table_size_q:
        Q['NaN'] = card_diff
        table_size_q += card_diff
    elif table_size_p < table_size_q:
        P['NaN'] = card_diff
        table_size_p += card_diff
    
    # values is the set of values in the alphabet
    values = P.index.union(Q.index, sort=False)
    
    missing_values = []
    for x in values:
        p_x = 0.0
        try:
            p_x = P[x]
        except:
            p_x = 0.0
        
        q_x = 0.0
        try:
            q_x = Q[x]
        except:
            q_x = 0.0
        # Ensure absolute continuity
        if q_x == 0.0 and p_x > 0.0:
            missing_values.append(x)

    if len(missing_values) > 0:
        table_size_q = table_size_q + len(missing_values)
        # for q_val in Q.index:
        #     old_prob = Q[q_val]
        #     freq = table_size_q*old_prob
        #     Q[q_val] = freq / new_size       
        new_vals = pd.Series(data=[1.0]*len(missing_values), index=missing_values)
        Q = pd.concat([Q, new_vals])

    assert(Q.sum() == table_size_q, f'Q: sum was: {Q.sum()} and expected {table_size_q}')
    assert(P.sum() == table_size_p, f'P: sum was: {P.sum()} and expected {table_size_p}')
    
        
    relative_entropy = 0.0
    for x in values:
        p_x = 0.0
        try:
            p_x = P[x] / table_size_p
        except:
            p_x = 0.0
        
        q_x = 0.0
        try:
            q_x = Q[x] / table_size_q
        except:
            q_x = 0.0

        if q_x == 0.0 and p_x > 0.0:
            raise ValueError("This should not happen...")

        if p_x > 0.0 and q_x > 0.0:
            relative_entropy += p_x*np.log2(p_x/q_x)
    return relative_entropy

def discretize_num_dist(dist: pd.Series, precision: int = 0):
    new_dist = {}
    for val in dist.index:
        num_val = val[0]
        disc_val = np.round(num_val, precision)
        try:
            new_dist[disc_val] = new_dist[disc_val] + dist[val]
        except:
            new_dist[disc_val] = dist[val]
    return pd.Series(new_dist)

def compute_prob_dist(table: pd.DataFrame, attr: str) -> pd.Series :
    dist = table[attr].value_counts(normalize=True, dropna=False)
    # Remove nan values from multiindex
    dist.index = pd.MultiIndex.from_frame(
        dist.index.to_frame().fillna(value='NaN')
    )
    return dist

def compute_freq_dist(table: pd.DataFrame, attr: str) -> pd.Series :
    dist = table[attr].value_counts(normalize=False, dropna=False)
    # Remove nan values from multiindex
    dist.index = pd.MultiIndex.from_frame(
        dist.index.to_frame().fillna(value='NaN')
    )
    return dist

def compute_dist(table: pd.DataFrame, attr: str) -> pd.Series :
    dist = table[attr].value_counts(dropna=False)
    # Remove nan values from multiindex
    dist.index = pd.MultiIndex.from_frame(
        dist.index.to_frame().fillna(value='NaN')
    )
    return dist, len(table)

def change_tuple_value(old_tuple, new_value, field):
    if type(old_tuple) != tuple:
        return new_value
    as_list = list(old_tuple)
    as_list[field] = new_value
    return tuple(as_list)

def specification_prob(dist, mf_inverse, masked_field=0):
    for i, x in enumerate(dist.index):
        if type(x) == tuple:
            msk_val = x[masked_field]
        elif type(x) == str:
            msk_val = x
        specification_list = mf_inverse(msk_val)
        values = []
        P = []
        p = dist[x]/len(specification_list)
        for sp_val in specification_list:
            new_x = change_tuple_value(x,sp_val,masked_field)
            values.append(new_x)
            P.append(p)
        specified_prob = pd.Series(data=P, index=values)   
         
        if i == 0:
            newDist = specified_prob
        else:
            newDist = pd.concat([newDist, specified_prob])
    return newDist

def filter_suppress(table, predicate, print_cardinality=True):
    result = table.copy()
    i=0
    for index, row in result.iterrows():
        keep = predicate(row)
        if not isinstance(keep, bool):
            raise ValueError("Predicate function did not return a boolean.")
        if not keep:
            result.loc[index, :] = "NaN"
        else:
            i+=1
    
    if print_cardinality:
        print("Cardinality after applying "+predicate.__name__+": "+str(i))
    return result

