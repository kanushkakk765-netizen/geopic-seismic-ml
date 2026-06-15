import segyio
import numpy as np
import matplotlib.pyplot as plt

SEGY_PATH = '../data/F3.segy'

print("Opening SEG-Y file...")

with segyio.open(SEGY_PATH, strict=False) as f:
    print('Total traces:', f.tracecount)
    print('Samples per trace:', len(f.samples))

    # Load all traces into a 2D array
    data = np.stack([f.trace[i] for i in range(f.tracecount)], axis=0)
    print('Data shape:', data.shape)

    # Convert 8-bit to float
    section = data.astype(np.float32)

    # Take middle chunk as our section
    mid = len(section) // 2
    start = max(0, mid - 200)
    end = min(len(section), mid + 200)
    section = section[start:end, :]
    print('Section shape:', section.shape)

    np.save('../outputs/section.npy', section)
    print('section.npy saved! ✅')

# Plot preview
plt.figure(figsize=(14, 6))
vmin = np.percentile(section, 2)
vmax = np.percentile(section, 98)
plt.imshow(section.T, cmap='Greys', aspect='auto',
           vmin=vmin, vmax=vmax, origin='upper')
plt.title('Raw Seismic Section — F3 Dutch')
plt.xlabel('Trace')
plt.ylabel('Time (samples)')
plt.colorbar(label='Amplitude')
plt.tight_layout()
plt.savefig('../outputs/raw_section.png', dpi=150)
plt.show()
print('Preview saved! ✅')