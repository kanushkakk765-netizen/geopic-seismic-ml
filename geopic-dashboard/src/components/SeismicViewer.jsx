import { useEffect, useRef, useState } from 'react';
import { fetchSection, fetchLabels } from '../api/client';

const COLORS = ['#E63946','#457B9D','#2A9D8F','#E9C46A','#F4A261'];

function hexToRgb(hex) {
    return [
        parseInt(hex.slice(1,3),16),
        parseInt(hex.slice(3,5),16),
        parseInt(hex.slice(5,7),16)
    ];
}

export default function SeismicViewer({ showOverlay, method }) {
    const canvasRef = useRef(null);
    const [section, setSection] = useState(null);
    const [cluster, setCluster] = useState(null);

    useEffect(() => {
        fetchSection().then(setSection);
        fetchLabels(method).then(setCluster);
    }, [method]);

    useEffect(() => {
        if (!section || !cluster) return;
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        canvas.width = section.width;
        canvas.height = section.height;
        const img = new window.Image();
        img.onload = () => {
            ctx.drawImage(img, 0, 0);
            if (showOverlay) {
                const imgData = ctx.getImageData(
                    0, 0, section.width, section.height);
                for (let y = 0; y < section.height; y++) {
                    for (let x = 0; x < section.width; x++) {
                        const label = cluster.labels[y][x];
                        const [r,g,b] = hexToRgb(
                            COLORS[label % COLORS.length]);
                        const i = (y * section.width + x) * 4;
                        imgData.data[i]   = (imgData.data[i]   + r) / 2;
                        imgData.data[i+1] = (imgData.data[i+1] + g) / 2;
                        imgData.data[i+2] = (imgData.data[i+2] + b) / 2;
                    }
                }
                ctx.putImageData(imgData, 0, 0);
            }
        };
        img.src = `data:image/png;base64,${section.image_b64}`;
    }, [section, cluster, showOverlay]);

    return (
        <canvas ref={canvasRef}
            style={{ width:'100%', border:'1px solid #ccc' }} />
    );
}