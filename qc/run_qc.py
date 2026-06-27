"""
qc/run_qc.py — Load F03 .wlt/.wll files and run QC
Run from project root: python qc/run_qc.py
"""
import pandas as pd
import numpy as np
import os, sys, glob, re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qc.scorer import score_well, summarise_well


def parse_two_col_file(filepath):
    """Parse DEPTH VALUE space-separated file (OpendTect .wlt/.wll format)."""
    depths, values = [], []
    with open(filepath, 'r', errors='ignore') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                try:
                    depths.append(float(parts[0]))
                    values.append(float(parts[1]))
                except ValueError:
                    continue
    return depths, values


def load_well(well_prefix, welldata_dir='welldata'):
    """
    Load all log files for a well prefix (e.g. 'F02-1').
    Combines all curves into one DataFrame keyed on DEPTH.
    """
    # Find all files matching this well
    patterns = [
        os.path.join(welldata_dir, f"{well_prefix}.wlt"),
        os.path.join(welldata_dir, f"{well_prefix}.wll"),
    ]
    # Also look for numbered curves: F02-1^1.wll, F02-1^2.wll etc.
    numbered = sorted(glob.glob(os.path.join(welldata_dir, f"{well_prefix}^*.wll")))
    all_files = [p for p in patterns if os.path.exists(p)] + numbered

    if not all_files:
        return None

    # Load each file as a curve
    combined = None
    curve_num = 0
    for fpath in all_files:
        depths, values = parse_two_col_file(fpath)
        if len(depths) < 10:
            continue
        curve_num += 1
        # Name curve by file suffix
        basename = os.path.basename(fpath)
        if '^' in basename:
            # e.g. F02-1^3.wll → CURVE_3
            num = re.search(r'\^(\d+)', basename)
            col = f"CURVE_{num.group(1)}" if num else f"CURVE_{curve_num}"
        elif basename.endswith('.wlt'):
            col = 'RHOB'  # .wlt is typically density/transit time
        else:
            col = f"CURVE_{curve_num}"

        df = pd.DataFrame({'DEPTH': depths, col: values})
        if combined is None:
            combined = df
        else:
            combined = pd.merge(combined, df, on='DEPTH', how='outer')

    if combined is not None:
        combined = combined.sort_values('DEPTH').reset_index(drop=True)
    return combined


def main():
    print("=" * 55)
    print("GEOPIC Well Log QC Tool — Phase 7")
    print("=" * 55)
    os.makedirs("outputs", exist_ok=True)

    welldata_dir = "welldata"

    # Find unique well prefixes from .wlt files (one per well)
    wlt_files = glob.glob(os.path.join(welldata_dir, "*.wlt"))
    well_prefixes = []
    for f in wlt_files:
        base = os.path.basename(f).replace('.wlt', '')
        well_prefixes.append(base)

    print(f"\nFound {len(well_prefixes)} wells: {well_prefixes[:5]}")

    results_summary = []
    all_scored = []

    for prefix in well_prefixes[:3]:  # process up to 3 wells
        print(f"\n📍 Processing: {prefix}")
        df = load_well(prefix, welldata_dir)

        if df is None or len(df) < 20:
            print(f"   ⚠️  Skipping — not enough data")
            continue

        print(f"   Loaded: {df.shape} — columns: {list(df.columns)}")
        scored = score_well(df)
        summary = summarise_well(scored)
        summary['well_name'] = prefix
        results_summary.append(summary)
        scored['well_name'] = prefix
        all_scored.append(scored)
        sc = summary['severity_counts']
        print(f"   ✅ RED={sc['RED']} YELLOW={sc['YELLOW']} "
              f"GREEN={sc['GREEN']} ({summary['pct_clean']}% clean)")

    if not results_summary:
        print("\n⚠️  No wells parsed — check welldata/ folder")
        return

    # Save outputs
    summary_df = pd.DataFrame(results_summary)
    summary_df.to_csv("outputs/qc_summary.csv", index=False)
    print(f"\n✅ Saved: outputs/qc_summary.csv")

    if all_scored:
        all_df = pd.concat(all_scored, ignore_index=True)
        flagged = all_df[all_df['severity'] != 'GREEN']
        flagged.to_csv("outputs/qc_flagged.csv", index=False)
        print(f"✅ Saved: outputs/qc_flagged.csv ({len(flagged)} flagged rows)")

    print("\n📊 QC Summary:")
    print(summary_df[['well_name','total_depths','pct_clean',
                       'severity_counts']].to_string(index=False))
    print("\n✅ Phase 7 QC complete!")

if __name__ == "__main__":
    main()
