"""
qc/scorer.py — Severity scoring combining all 5 detectors
"""
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qc.detectors import (detect_spikes, detect_flat_lines, detect_cycle_skips,
                           detect_washed_out, detect_impossible_values)

def score_well(df):
    result = df.copy()
    flag_cols = []

    # Run detectors on every numeric column except DEPTH
    value_cols = [c for c in df.columns if c != 'DEPTH']

    spike_flags = pd.Series(False, index=df.index)
    flat_flags  = pd.Series(False, index=df.index)
    skip_flags  = pd.Series(False, index=df.index)
    wash_flags  = pd.Series(False, index=df.index)
    impo_flags  = pd.Series(False, index=df.index)

    for col in value_cols:
        spike_flags |= detect_spikes(df[col])
        flat_flags  |= detect_flat_lines(df[col])
        skip_flags  |= detect_cycle_skips(df[col])
        wash_flags  |= detect_washed_out(df[col])
        impo_flags  |= detect_impossible_values(df[col], col)

    result['spike']           = spike_flags
    result['flat_line']       = flat_flags
    result['cycle_skip']      = skip_flags
    result['washed_out']      = wash_flags
    result['impossible_value']= impo_flags

    flag_cols = ['spike','flat_line','cycle_skip','washed_out','impossible_value']
    result['flag_count'] = result[flag_cols].sum(axis=1)
    result['severity'] = result['flag_count'].apply(
        lambda c: 'RED' if c >= 2 else ('YELLOW' if c == 1 else 'GREEN'))
    return result

def summarise_well(scored_df):
    counts = scored_df['severity'].value_counts().to_dict()
    total  = len(scored_df)
    return {
        'total_depths': total,
        'severity_counts': {
            'RED':    counts.get('RED', 0),
            'YELLOW': counts.get('YELLOW', 0),
            'GREEN':  counts.get('GREEN', 0),
        },
        'pct_clean': round(counts.get('GREEN', 0) / total * 100, 1)
    }
