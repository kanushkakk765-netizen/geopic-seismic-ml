import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

section = np.load('../outputs/section.npy')
labels  = np.load('../outputs/label_map_kmeans.npy')
K = 5

COLORS = ['#E63946','#457B9D','#2A9D8F','#E9C46A','#F4A261']
cmap   = mcolors.ListedColormap(COLORS[:K])

fig, axes = plt.subplots(1, 2, figsize=(18, 8))

vmin = np.percentile(section, 2)
vmax = np.percentile(section, 98)

# Left - raw seismic
axes[0].imshow(section.T, cmap='Greys', aspect='auto',
               vmin=vmin, vmax=vmax, origin='upper')
axes[0].set_title('Raw Seismic Section')
axes[0].set_xlabel('Crossline')
axes[0].set_ylabel('Time (samples)')

# Right - facies overlay
axes[1].imshow(section.T, cmap='Greys', aspect='auto',
               vmin=vmin, vmax=vmax, origin='upper', alpha=0.4)
axes[1].imshow(labels.T, cmap=cmap, aspect='auto',
               alpha=0.6, origin='upper', vmin=0, vmax=K-1)
axes[1].set_title(f'Facies Map — K-Means (k={K})')
axes[1].set_xlabel('Crossline')

plt.tight_layout()
plt.savefig('../outputs/facies_map.png', dpi=150)
plt.show()
print('Facies map saved! ✅')
