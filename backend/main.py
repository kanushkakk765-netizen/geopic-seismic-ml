from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='GEOPIC API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/health')
def health():
    return {'status': 'ok', 'message': 'GEOPIC API is running!'}
import numpy as np
import base64, io
from pathlib import Path
from PIL import Image

OUTPUTS = Path('../outputs')

# Endpoint 1 - seismic section image
@app.get('/api/seismic-section')
def get_section(downsample: int = 4):
    section = np.load(OUTPUTS / 'section.npy')
    s = section[::downsample, ::downsample]
    vmin, vmax = np.percentile(s, 2), np.percentile(s, 98)
    norm = np.clip((s - vmin) / (vmax - vmin), 0, 1)
    img_array = (norm * 255).astype(np.uint8)
    img = Image.fromarray(img_array.T)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    b64 = base64.b64encode(buf.getvalue()).decode()
    return {
        'image_b64': b64,
        'width': img_array.shape[0],
        'height': img_array.shape[1]
    }

# Endpoint 2 - cluster labels
@app.get('/api/cluster-labels')
def get_labels(method: str = 'kmeans', downsample: int = 4):
    fname = 'label_map_kmeans.npy' if method == 'kmeans' \
            else 'label_map_gmm.npy'
    labels = np.load(OUTPUTS / fname)
    labels_ds = labels[::downsample, ::downsample]
    return {
        'labels': labels_ds.T.tolist(),
        'n_clusters': int(labels.max() + 1),
        'method': method
    }

# Endpoint 3 - attribute statistics
@app.get('/api/attribute-stats')
def get_stats():
    X      = np.load(OUTPUTS / 'feature_matrix.npy')
    labels = np.load(OUTPUTS / 'kmeans_labels.npy')
    names  = ['envelope','inst_phase','cosine_phase',
              'inst_freq','rms','refl_strength','sweetness','raw_amp']
    k = int(labels.max() + 1)
    stats = {}
    for i in range(k):
        mask = labels == i
        stats[str(i)] = {
            'mean':  X[mask].mean(axis=0).tolist(),
            'std':   X[mask].std(axis=0).tolist(),
            'count': int(mask.sum())
        }
    return {'features': names, 'clusters': stats}

# Endpoint 4 - t-SNE data
@app.get('/api/tsne')
def get_tsne():
    X      = np.load(OUTPUTS / 'feature_matrix.npy')
    labels = np.load(OUTPUTS / 'kmeans_labels.npy')
    from sklearn.manifold import TSNE
    np.random.seed(42)
    idx    = np.random.choice(len(X), 10000, replace=False)
    X_2d   = TSNE(n_components=2, random_state=42).fit_transform(X[idx])
    return {
        'x':      X_2d[:, 0].tolist(),
        'y':      X_2d[:, 1].tolist(),
        'labels': labels[idx].tolist()
    }