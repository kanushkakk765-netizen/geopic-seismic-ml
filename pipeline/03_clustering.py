import numpy as np
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture

print("Loading feature matrix...")
X      = np.load('../outputs/feature_matrix.npy')
section = np.load('../outputs/section.npy')
print('Feature matrix shape:', X.shape)

K = 5  # number of clusters

# K-Means
print("Running K-Means...")
km = KMeans(n_clusters=K, random_state=42, n_init=10)
kmeans_labels = km.fit_predict(X)
np.save('../outputs/kmeans_labels.npy', kmeans_labels)
print('K-Means done! ✅')

# GMM
print("Running GMM...")
gmm = GaussianMixture(n_components=K, random_state=42,
                      covariance_type='diag', max_iter=200)
gmm.fit(X)
gmm_labels = gmm.predict(X)
np.save('../outputs/gmm_labels.npy', gmm_labels)
print('GMM done! ✅')

# Reshape to 2D
label_map_km  = kmeans_labels.reshape(section.shape)
label_map_gmm = gmm_labels.reshape(section.shape)
np.save('../outputs/label_map_kmeans.npy', label_map_km)
np.save('../outputs/label_map_gmm.npy', label_map_gmm)
print('Label maps saved! ✅')