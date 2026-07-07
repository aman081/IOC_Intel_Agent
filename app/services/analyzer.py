import json
from sqlalchemy.orm import Session
from app.models import AnalysisHistory
from app.schemas import SourceResult, AnalyzeResponse
from app.services.classifier import classify_ioc, normalize_ioc
from app.services.cache import get_cached_result, set_cached_result
from app.services.virustotal import VirusTotalClient
from app.services.abuseipdb import AbuseIPDBClient
from app.services.scorer import score_ioc, verdict_from_score, recommendation_from_verdict


async def analyze_ioc(db: Session, raw_ioc: str) -> AnalyzeResponse:
    normalized = normalize_ioc(raw_ioc)
    ioc_type = classify_ioc(normalized)

    if ioc_type == "UNKNOWN":
        return AnalyzeResponse(
            ioc=raw_ioc,
            normalized_ioc=normalized,
            type=ioc_type,
            score=0,
            verdict="Invalid",
            reasons=["IOC format is not recognized."],
            recommendation="Check the IOC value and submit a valid IP, URL, domain, MD5, SHA1, or SHA256.",
            sources={},
        )

    sources: dict[str, SourceResult] = {}

    vt_cached = get_cached_result(db, normalized, "virustotal")
    if vt_cached is not None:
        vt_result = vt_cached
        sources["virustotal"] = SourceResult(source="virustotal", available=vt_result.get("available", False), cached=True, data=vt_result)
    else:
        vt_result = await VirusTotalClient().lookup(normalized, ioc_type)
        set_cached_result(db, normalized, ioc_type, "virustotal", vt_result)
        sources["virustotal"] = SourceResult(source="virustotal", available=vt_result.get("available", False), cached=False, data=vt_result, error=vt_result.get("error"))

    abuse_result = None
    if ioc_type == "IP":
        abuse_cached = get_cached_result(db, normalized, "abuseipdb")
        if abuse_cached is not None:
            abuse_result = abuse_cached
            sources["abuseipdb"] = SourceResult(source="abuseipdb", available=abuse_result.get("available", False), cached=True, data=abuse_result)
        else:
            abuse_result = await AbuseIPDBClient().lookup(normalized, ioc_type)
            set_cached_result(db, normalized, ioc_type, "abuseipdb", abuse_result)
            sources["abuseipdb"] = SourceResult(source="abuseipdb", available=abuse_result.get("available", False), cached=False, data=abuse_result, error=abuse_result.get("error"))

    score, reasons = score_ioc(ioc_type, vt_result, abuse_result)
    verdict = verdict_from_score(score)
    recommendation = recommendation_from_verdict(verdict)

    history = AnalysisHistory(
        ioc=raw_ioc,
        normalized_ioc=normalized,
        ioc_type=ioc_type,
        score=score,
        verdict=verdict,
        reason=" | ".join(reasons),
        sources_json=json.dumps({k: v.model_dump() for k, v in sources.items()}, default=str),
    )
    db.add(history)
    db.commit()

    return AnalyzeResponse(
        ioc=raw_ioc,
        normalized_ioc=normalized,
        type=ioc_type,
        score=score,
        verdict=verdict,
        reasons=reasons,
        recommendation=recommendation,
        sources=sources,
    )
