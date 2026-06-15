import { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import { fetchTSNE } from '../api/client';

const COLORS = ['#E63946','#457B9D','#2A9D8F','#E9C46A','#F4A261'];

export default function TSNEPlot({ nClusters }) {
    const [data, setData] = useState(null);

    useEffect(() => { fetchTSNE().then(setData); }, []);

    if (!data) return <p>Loading t-SNE...</p>;

    const traces = Array.from({ length: nClusters }, (_, k) => ({
        x: data.x.filter((_,i) => data.labels[i] === k),
        y: data.y.filter((_,i) => data.labels[i] === k),
        mode: 'markers',
        marker: { color: COLORS[k], size: 3, opacity: 0.6 },
        name: `Cluster ${k}`,
        type: 'scatter'
    }));

    return (
        <Plot data={traces}
            layout={{ title:'t-SNE Cluster View',
                height:400, margin:{ t:40 } }}
            style={{ width:'100%' }} />
    );
}