# IOC Threat Assessment Agent

# Table of Contents
1. Executive Summary
2. Problem Statement
3. Solution Overview
4. Features
5. Technology Stack
6. Architecture
7. Project Structure
8. Data Flow
9. IOC Types Supported
10. Threat Intelligence Sources
11. Scoring Engine
12. Database Design
13. Backend APIs
14. Streamlit UI
15. Excel Report Generator
16. Docker Deployment
17. Environment Variables
18. Sample Inputs and Outputs
19. Troubleshooting
20. Security Considerations
21. Future Enhancements
22. Demo Walkthrough
23. Developer Notes

---

# 1. Executive Summary

IOC Threat Assessment Agent is a security automation platform built using FastAPI, Streamlit, SQLite, Docker, VirusTotal and AbuseIPDB.

The objective of the platform is to ingest Indicators of Compromise (IOCs), enrich them using external threat intelligence sources, calculate a risk score, generate actionable security recommendations and export analyst-friendly reports.

The solution supports:

- Single IOC Analysis
- Bulk IOC Analysis
- Threat Intelligence Enrichment
- IOC Risk Scoring
- IOC History
- IOC Cache
- Automated XLSX Report Generation
- Dockerized Deployment

This project simulates a real-world SOC analyst workflow.

---

# 2. Problem Statement

SOC analysts frequently receive IOC feeds consisting of:

- IP Addresses
- Domains
- URLs
- MD5 Hashes
- SHA1 Hashes
- SHA256 Hashes

Analysts then manually check:

- VirusTotal
- AbuseIPDB
- Internal Intelligence Sources

This process is repetitive and time consuming.

The purpose of this project is to automate:

Input IOC -> Enrichment -> Scoring -> Recommendation -> Reporting

---

# 3. Solution Overview

The application consists of:

Frontend:
- Streamlit

Backend:
- FastAPI

Database:
- SQLite

Threat Intelligence:
- VirusTotal
- AbuseIPDB

Deployment:
- Docker Compose

---

# 4. Features

## Single IOC Analysis

Allows analysts to analyze a single IOC.

Examples:

8.8.8.8

google.com

44d88612fea8a8f36de82e1278abb02f

## Bulk IOC Analysis

Upload CSV/XLSX files.

## IOC Classification

Automatically identifies IOC type.

## Threat Intelligence Enrichment

Queries external data sources.

## IOC Cache

Stores previous responses.

## History

Stores analysis history.

## Excel Report Generator

Generates multi-sheet SOC style reports.

---

# 5. Technology Stack

## Backend

FastAPI
Uvicorn
SQLAlchemy
Pydantic
Pydantic Settings
Httpx

## Frontend

Streamlit
Pandas
Requests

## Database

SQLite

## Reporting

OpenPyXL
Pandas

## Deployment

Docker
Docker Compose

---

# 6. Architecture

User
 |
 v
Streamlit UI
 |
 v
FastAPI API Layer
 |
 +---- IOC Classifier
 |
 +---- Cache Layer
 |
 +---- VirusTotal Service
 |
 +---- AbuseIPDB Service
 |
 +---- Scoring Engine
 |
 +---- Report Generator
 |
 v
SQLite

---

# 7. Project Structure

```text
app/
├── main.py
├── config.py
├── database.py
├── models.py
├── schemas.py
└── services/
    ├── analyzer.py
    ├── classifier.py
    ├── cache.py
    ├── virustotal.py
    ├── abuseipdb.py
    ├── scorer.py
    └── report_generator.py

ui/
└── streamlit_app.py
```

---

# 8. Data Flow

1. IOC submitted
2. IOC normalized
3. IOC classified
4. Cache lookup
5. VirusTotal query
6. AbuseIPDB query (IPs only)
7. Score calculation
8. Verdict generation
9. History storage
10. UI response
11. Report generation

---

# 9. IOC Types Supported

## IP Address

Examples:

8.8.8.8
1.1.1.1

## Domain

google.com

## URL

https://example.com

## MD5

44d88612fea8a8f36de82e1278abb02f

## SHA1

3395856ce81f2b7382dee72602f798b642f14140

## SHA256

275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f

---

# 10. Threat Intelligence Sources

## VirusTotal

Data Used:

- Malicious detections
- Suspicious detections
- Reputation
- Tags
- Last Analysis Date

## AbuseIPDB

Data Used:

- Abuse Confidence Score
- Report Count
- ISP
- Country
- TOR Status
- Usage Type

---

# 11. Scoring Engine

The scoring engine combines indicators from multiple sources.

Signals:

- VirusTotal malicious detections
- VirusTotal suspicious detections
- VirusTotal reputation
- VirusTotal tags
- AbuseIPDB confidence score
- TOR indicators

Verdicts:

0-20 Clean
21-50 Suspicious
51-80 Malicious
81-100 Critical

Example:

EICAR MD5:

44d88612fea8a8f36de82e1278abb02f

Expected Verdict:
Critical

---

# 12. Database Design

## IOCCache

Stores cached TI responses.

Columns:

- id
- ioc
- ioc_type
- source
- response_json
- fetched_at
- ttl_until

## AnalysisHistory

Columns:

- id
- ioc
- normalized_ioc
- ioc_type
- score
- verdict
- reason
- sources_json
- created_at

---

# 13. Backend APIs

## GET /health

Health Check.

Response:

```json
{
  "status":"healthy"
}
```

## POST /analyze

Request:

```json
{
  "ioc":"8.8.8.8"
}
```

## POST /bulk-analyze

Accepts CSV/XLSX.

## POST /generate-report

Returns:

IOC_Threat_Report.xlsx

## GET /history

Returns history records.

## DELETE /history

Deletes history.

---

# 14. Streamlit UI

Pages:

## Single IOC

Displays:

- Type
- Score
- Verdict
- Recommendation
- Source Results

## Bulk Upload

Supports:

- Analyze File
- Download CSV
- Download XLSX
- Generate SOC Report

## History

- View History
- Delete History

---

# 15. Excel Report Generator

Generated File:

IOC_Threat_Report.xlsx

Sheets:

## Executive Summary

Contains:

- Total IOC Count
- Highest Risk IOC
- Verdict Distribution

## IOC Results

Full IOC table.

## Threat Intel Details

Raw intelligence details.

## Recommendations

Analyst actions.

---

# 16. Docker Deployment

Build:

```bash
docker compose build
```

Start:

```bash
docker compose up
```

Detached:

```bash
docker compose up -d
```

UI:

http://localhost:8501

Swagger:

http://localhost:8000/docs

---

# 17. Environment Variables

```env
VIRUSTOTAL_API_KEY=
ABUSEIPDB_API_KEY=
DATABASE_URL=sqlite:///./data/ioc_agent.db
CACHE_TTL_HOURS=24
ABUSEIPDB_MAX_AGE_DAYS=90
FASTAPI_BASE_URL=http://api:8000
```

---

# 18. Sample Input and Output

## Input CSV

```csv
ioc
8.8.8.8
google.com
44d88612fea8a8f36de82e1278abb02f
```

Output Columns:

- IOC
- Type
- Score
- Verdict
- Recommendation

---

# 19. Troubleshooting

## API Container Crash

Check:

docker compose logs api

## UI Cannot Connect To Backend

Ensure:

FASTAPI_BASE_URL=http://api:8000

## API Keys Missing

Verify .env is mounted.

---

# 20. Security Considerations

- Do not commit .env files.
- Do not expose API keys.
- Avoid uploading confidential internal IOCs.
- Use Docker secrets in production.

Recommended .gitignore:

```gitignore
.env
*.db
__pycache__/
data/
```

---

# 21. Future Enhancements

- URLScan Integration
- Hybrid Analysis
- Any.Run
- Authentication
- RBAC
- PDF Reports
- SIEM Query Generator
- Threat Graph Visualization

---

# 22. Demo Walkthrough

1. Start Docker Compose.
2. Open Streamlit.
3. Analyze google.com.
4. Analyze 8.8.8.8.
5. Analyze EICAR hash.
6. Upload CSV.
7. Generate Report.
8. Open IOC_Threat_Report.xlsx.

---

# 23. Developer Notes

This project demonstrates:

- FastAPI Development
- Streamlit Development
- Docker Deployment
- API Integration
- Threat Intelligence Enrichment
- IOC Classification
- Security Automation
- Report Generation
- SOC Workflow Automation

The solution is intentionally modular and can be extended with additional intelligence providers, authentication mechanisms, sandbox integrations and enterprise workflows.
