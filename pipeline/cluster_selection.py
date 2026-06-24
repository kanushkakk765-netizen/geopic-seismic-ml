"""
pipeline/cluster_selection.py
Phase 3 missing piece — Elbow + Silhouette plot to justify k=5
Run from project root: python pipeline/cluster_selection.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Load feature matrix
print("Loading feature matrix...")
X = np.load("outputs/feature_matrix.npy")
print(f"Feature matrix shape: {X.shape}")

# Use a sample for speed (5000 points is enough for k-selection)
np.random.seed(42)
idx = np.random.choice(len(X), min(5000, len(X)), replace=False)
X_sample = X[idx]

# Standardize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_sample)

# Test k = 2 to 9
k_range = range(2, 10)
inertias = []
silhouettes = []

print("Computing elbow and silhouette scores...")
for k in k_range:
    print(f"  k={k}...", end=" ", flush=True)
    km = KMeans(n_clusters=k, random_state=42, n_init=5, max_iter=100)
    labels = km.fit_predict(X_scaled)
    inertias.append(km.inertia_)
    sil = silhouette_score(X_scaled, labels, sample_size=2000, random_state=42)
    silhouettes.append(sil)
    print(f"inertia={km.inertia_:.0f}, silhouette={sil:.3f}")

# Plot
fig = plt.figure(figsize=(12, 5))
fig.patch.set_facecolor('#0f1117')
gs = gridspec.GridSpec(1, 2, figure=fig)

# Elbow plot
ax1 = fig.add_subplot(gs[0])
ax1.set_facecolor('#1a1d2e')
ax1.plot(list(k_range), inertias, 'o-', color='#4fc3f7', linewidth=2.5,
         markersize=7, markerfacecolor='white', markeredgecolor='#4fc3f7')
ax1.axvline(x=5, color='#ff6b6b', linestyle='--', linewidth=1.5, alpha=0.8)
ax1.annotate('k = 5\n(selected)', xy=(5, inertias[3]),
             xytext=(6.2, inertias[3] * 1.05),
             fontsize=9, color='#ff6b6b',
             arrowprops=dict(arrowstyle='->', color='#ff6b6b', lw=1.2))
ax1.set_title('Elbow Method — Inertia vs k', color='white', fontsize=12, pad=10)
ax1.set_xlabel('Number of Clusters (k)', color='#aaaaaa', fontsize=10)
ax1.set_ylabel('Inertia (Within-cluster SSE)', color='#aaaaaa', fontsize=10)
ax1.tick_params(colors='#aaaaaa')
ax1.set_xticks(list(k_range))
for spine in ax1.spines.values():
    spine.set_edgecolor('#333355')
ax1.grid(True, alpha=0.15, color='white')

# Silhouette plot
ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor('#1a1d2e')
ax2.plot(list(k_range), silhouettes, 's-', color='#a5d6a7', linewidth=2.5,
         markersize=7, markerfacecolor='white', markeredgecolor='#a5d6a7')
ax2.axvline(x=5, color='#ff6b6b', linestyle='--', linewidth=1.5, alpha=0.8)
ax2.annotate('k = 5\n(selected)', xy=(5, silhouettes[3]),
             xytext=(6.2, silhouettes[3] * 0.97),
             fontsize=9, color='#ff6b6b',
             arrowprops=dict(arrowstyle='->', color='#ff6b6b', lw=1.2))
ax2.set_title('Silhouette Score vs k', color='white', fontsize=12, pad=10)
ax2.set_xlabel('Number of Clusters (k)', color='#aaaaaa', fontsize=10)
ax2.set_ylabel('Silhouette Score (higher = better)', color='#aaaaaa', fontsize=10)
ax2.tick_params(colors='#aaaaaa')
ax2.set_xticks(list(k_range))
for spine in ax2.spines.values():
    spine.set_edgecolor('#333355')
ax2.grid(True, alpha=0.15, color='white')

plt.suptitle('K-Means Cluster Selection — F3 Block Seismic Facies',
             color='white', fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('outputs/cluster_selection.png', dpi=150,
            bbox_inches='tight', facecolor='#0f1117')
print("\n✅ Saved: outputs/cluster_selection.png")
plt.close()

# Print summary table
print("\n📊 Summary:")
print(f"{'k':>4} {'Inertia':>12} {'Silhouette':>12}")
print("-" * 30)
for k, inn, sil in zip(k_range, inertias, silhouettes):
    marker = " ← selected" if k == 5 else ""
    print(f"{k:>4} {inn:>12.0f} {sil:>12.3f}{marker}")