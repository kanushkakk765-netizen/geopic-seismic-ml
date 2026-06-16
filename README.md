# GEOPIC Seismic Facies Dashboard

**ONGC GEOPIC Internship 2026 — Programming Division**

Built by Kanushka Katariya | Uttaranchal University— B.Tech CSE, 2nd Year

## Project Overview
An end-to-end geoscience ML pipeline that:
- Reads real F3 Block 3D seismic data (SEG-Y format)
- Extracts 8 seismic attributes using Hilbert Transform
- Applies K-Means & GMM clustering to classify geological facies
- Serves results via FastAPI REST API
- Displays interactive dashboard in React

## Tech Stack
Python, segyio, scikit-learn, FastAPI, React, Plotly.js, NumPy, Pandas

## Project Structure
- `pipeline/` — ML pipeline scripts (load → attributes → clustering → visualise)
- `backend/` — FastAPI REST API server
- `geopic-dashboard/` — React interactive dashboard
- `outputs/` — Generated PNG maps and NPY arrays
- `welldata/` — F3 well log data for validation

## How to Run
### Backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```
### Frontend
```bash
cd geopic-dashboard
npm run dev
```