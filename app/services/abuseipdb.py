import httpx
from app.config import settings


class AbuseIPDBClient:
    BASE_URL = "https://api.abuseipdb.com/api/v2/check"

    def __init__(self):
        self.api_key = settings.abuseipdb_api_key

    def _headers(self):
        return {"Key": self.api_key or "", "Accept": "application/json"}

    async def lookup(self, ioc: str, ioc_type: str) -> dict:
        if ioc_type != "IP":
            return {"available": False, "error": "AbuseIPDB supports IP addresses only"}
        if not self.api_key:
            return {"available": False, "error": "AbuseIPDB API key not configured"}

        params = {
            "ipAddress": ioc,
            "maxAgeInDays": settings.abuseipdb_max_age_days,
            "verbose": "",
        }
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(self.BASE_URL, headers=self._headers(), params=params)

        if resp.status_code == 429:
            return {"available": False, "error": "AbuseIPDB rate limit exceeded"}
        if resp.status_code >= 400:
            return {"available": False, "error": f"AbuseIPDB error {resp.status_code}: {resp.text[:300]}"}

        data = resp.json().get("data", {})
        return {
            "available": True,
            "abuse_confidence_score": int(data.get("abuseConfidenceScore", 0) or 0),
            "total_reports": int(data.get("totalReports", 0) or 0),
            "num_distinct_users": int(data.get("numDistinctUsers", 0) or 0),
            "is_tor": bool(data.get("isTor", False)),
            "country_code": data.get("countryCode"),
            "usage_type": data.get("usageType"),
            "isp": data.get("isp"),
            "domain": data.get("domain"),
            "last_reported_at": data.get("lastReportedAt"),
        }
