export default function Controls({
    showOverlay, setShowOverlay, method, setMethod }) {
    return (
        <div style={{ display:'flex', gap:'12px', margin:'16px 0' }}>
            <button onClick={() => setShowOverlay(!showOverlay)}
                style={{
                    background: showOverlay ? '#2E75B6' : '#ddd',
                    color: showOverlay ? 'white' : 'black',
                    padding:'8px 16px', border:'none',
                    borderRadius:'6px', cursor:'pointer'
                }}>
                {showOverlay ? 'Hide Overlay' : 'Show Overlay'}
            </button>
            <select value={method}
                onChange={e => setMethod(e.target.value)}
                style={{ padding:'8px', borderRadius:'6px' }}>
                <option value="kmeans">K-Means</option>
                <option value="gmm">GMM</option>
            </select>
        </div>
    );
}