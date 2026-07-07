from io import BytesIO
import pandas as pd
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.models import AnalysisHistory, IOCCache
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.analyzer import analyze_ioc

Base.metadata.create_all(bind=engine)

app = FastAPI(title="IOC Threat Assessment Agent", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(payload: AnalyzeRequest, db: Session = Depends(get_db)):
    return await analyze_ioc(db, payload.ioc)


@app.post("/bulk-analyze")
async def bulk_analyze(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    filename = (file.filename or "").lower()

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(contents))
        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(BytesIO(contents), engine="openpyxl" if filename.endswith(".xlsx") else None)
        else:
            raise HTTPException(status_code=400, detail="Upload CSV or XLSX file only.")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not read file: {exc}")

    if df.empty:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    ioc_col = "ioc" if "ioc" in [str(c).lower() for c in df.columns] else df.columns[0]
    if ioc_col == "ioc":
        # recover original column name if it differs by case
        ioc_col = next(c for c in df.columns if str(c).lower() == "ioc")

    results = []
    for value in df[ioc_col].dropna().astype(str).tolist():
        result = await analyze_ioc(db, value)
        results.append(result.model_dump())

    flat_rows = []
    for r in results:
        flat_rows.append({
            "ioc": r["ioc"],
            "normalized_ioc": r["normalized_ioc"],
            "type": r["type"],
            "score": r["score"],
            "verdict": r["verdict"],
            "reasons": " | ".join(r["reasons"]),
            "recommendation": r["recommendation"],
        })

    return {"count": len(results), "results": results, "table": flat_rows}


@app.get("/history")
def history(limit: int = 50, db: Session = Depends(get_db)):
    rows = (
        db.query(AnalysisHistory)
        .order_by(AnalysisHistory.created_at.desc())
        .limit(min(limit, 500))
        .all()
    )
    return [
        {
            "id": r.id,
            "ioc": r.ioc,
            "normalized_ioc": r.normalized_ioc,
            "type": r.ioc_type,
            "score": r.score,
            "verdict": r.verdict,
            "reason": r.reason,
            "created_at": r.created_at.isoformat(),
        }
        for r in rows
    ]


@app.delete("/history")
def clear_history(db: Session = Depends(get_db)):

    db.query(AnalysisHistory).delete()

    db.query(IOCCache).delete()

    db.commit()

    return {
        "message": "History and cache cleared successfully."
    }
