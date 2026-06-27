"""
qc/detectors.py — 5 artifact detectors for well log QC
"""
import numpy as np
import pandas as pd

def detect_spikes(curve, window=20, n_sigma=3):
    curve = pd.to_numeric(curve, errors='coerce')
    roll_mean = curve.rolling(window=window, center=True, min_periods=3).mean()
    roll_std  = curve.rolling(window=window, center=True, min_periods=3).std()
    spikes = (curve > roll_mean + n_sigma*roll_std) | (curve < roll_mean - n_sigma*roll_std)
    return spikes.fillna(False)

def detect_flat_lines(curve, window=10, tol=1e-6):
    curve = pd.to_numeric(curve, errors='coerce')
    flat = curve.rolling(window=window, min_periods=3).std() < tol
    return flat.fillna(False)

def detect_cycle_skips(curve, threshold=50):
    curve = pd.to_numeric(curve, errors='coerce')
    return (curve.diff().abs() > threshold).fillna(False)

def detect_washed_out(curve, threshold_low=None, threshold_high=None):
    curve = pd.to_numeric(curve, errors='coerce')
    if threshold_low is None:
        threshold_low = curve.quantile(0.05)
    return (curve < threshold_low).fillna(False)

def detect_impossible_values(curve, curve_type):
    curve = pd.to_numeric(curve, errors='coerce')
    bounds = {
        'RHOB': (1.0, 3.5),
        'NPHI': (-0.05, 1.0),
        'GR':   (0.0, 500.0),
        'DTC':  (40.0, 240.0),
        'CALI': (4.0, 30.0),
    }
    ctype = curve_type.upper()
    for key, (lo, hi) in bounds.items():
        if key in ctype:
            return ((curve < lo) | (curve > hi)).fillna(False)
    return pd.Series(False, index=curve.index)
