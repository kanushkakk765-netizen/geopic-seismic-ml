import { useState } from 'react';
import SeismicViewer from './components/SeismicViewer';
import TSNEPlot from './components/TSNEPlot';
import Controls from './components/Controls';

export default function App() {
    const [showOverlay, setShowOverlay] = useState(false);
    const [method, setMethod] = useState('kmeans');

    return (
        <div style={{ maxWidth:'1100px', margin:'0 auto',
                      padding:'24px', fontFamily:'sans-serif' }}>
            <h1 style={{ color:'#1F4E79' }}>
                GEOPIC Seismic Facies Dashboard
            </h1>
            <p style={{ color:'#666' }}>
                F3 Block · Netherlands North Sea ·
                ONGC GEOPIC Internship 2026
            </p>
            <hr />

            <h2>Seismic Section</h2>
            <Controls
                showOverlay={showOverlay}
                setShowOverlay={setShowOverlay}
                method={method}
                setMethod={setMethod} />
            <SeismicViewer
                showOverlay={showOverlay}
                method={method} />

            <h2 style={{ marginTop:'40px' }}>
                Cluster Separation (t-SNE)
            </h2>
            <TSNEPlot nClusters={5} />
        </div>
    );
}