import numpy as np
import matplotlib.pyplot as plt
import struct
import os

WELL_DIR = '../welldata'

def read_wll_file(filepath):
    """Read OpenDTect .wll well log file"""
    logs = {}
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        # Parse binary well log data
        offset = 0
        values = []
        while offset + 4 <= len(data):
            try:
                val = struct.unpack_from('>f', data, offset)[0]
                if -99999 < val < 99999:
                    values.append(val)
                offset += 4
            except:
                offset += 1
        return np.array(values, dtype=np.float32)
    except Exception as e:
        print(f'Error reading {filepath}: {e}')
        return None

# Find all F03 well files
print("Scanning well data folder...")
wll_files = [f for f in os.listdir(WELL_DIR) 
             if f.startswith('F03') and f.endswith('.wll')]
print(f'Found {len(wll_files)} F03 well log files')

# Read all logs
all_logs = {}
for fname in sorted(wll_files):
    fpath = os.path.join(WELL_DIR, fname)
    data = read_wll_file(fpath)
    if data is not None and len(data) > 10:
        all_logs[fname] = data
        print(f'  {fname}: {len(data)} samples, '
              f'range [{data.min():.1f}, {data.max():.1f}]')

print(f'\nSuccessfully loaded {len(all_logs)} logs')

# Plot the well logs
if all_logs:
    fig, axes = plt.subplots(1, min(4, len(all_logs)), 
                              figsize=(14, 10), sharey=True)
    if len(all_logs) == 1:
        axes = [axes]
    
    colors = ['#E63946', '#457B9D', '#2A9D8F', '#E9C46A']
    
    for idx, (fname, data) in enumerate(list(all_logs.items())[:4]):
        ax = axes[idx]
        depth = np.arange(len(data))
        ax.plot(data, depth, color=colors[idx % 4], linewidth=0.8)
        ax.set_title(fname.replace('.wll', ''), fontsize=8)
        ax.set_xlabel('Value')
        ax.invert_yaxis()
        ax.grid(True, alpha=0.3)
        if idx == 0:
            ax.set_ylabel('Sample depth')

    plt.suptitle('F03 Well Logs — Netherlands North Sea',
                 fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig('../outputs/well_logs.png', dpi=150)
    plt.show()
    print('Well log plot saved! ✅')

    # Save for API
    log_data = {k: v.tolist() for k, v in all_logs.items()}
    np.save('../outputs/well_logs.npy', log_data)
    print('well_logs.npy saved! ✅')