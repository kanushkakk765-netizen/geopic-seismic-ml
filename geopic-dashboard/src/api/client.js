const BASE = 'https://geopic-seismic-backend.onrender.com';

export const fetchSection = () =>
    fetch(`${BASE}/api/seismic-section`).then(r => r.json());

export const fetchLabels = (method = 'kmeans') =>
    fetch(`${BASE}/api/cluster-labels?method=${method}`).then(r => r.json());

export const fetchStats = () =>
    fetch(`${BASE}/api/attribute-stats`).then(r => r.json());

export const fetchTSNE = () =>
    fetch(`${BASE}/api/tsne`).then(r => r.json());