# IOC Threat Assessment Agent

FastAPI + SQLite + Streamlit MVP for IOC enrichment using VirusTotal and AbuseIPDB.

## Features
- Single IOC analysis
- Bulk CSV/XLSX analysis
- IOC classifier: IP, URL, domain, MD5, SHA1, SHA256
- SQLite cache with TTL
- Analysis history
- Unified risk score and verdict
- Streamlit minimal UI

## Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and add API keys.

## Run backend

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Run UI

```bash
streamlit run ui/streamlit_app.py
```

## API examples

```bash
curl -X POST http://127.0.0.1:8000/analyze   -H "Content-Type: application/json"   -d '{"ioc":"8.8.8.8"}'
```

Bulk CSV must contain either an `ioc` column or the IOC values in the first column.
