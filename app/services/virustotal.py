import base64
import httpx
from app.config import settings


class VirusTotalClient:
    BASE_URL = "https://www.virustotal.com/api/v3"

    def __init__(self):
        self.api_key = settings.virustotal_api_key

    @staticmethod
    def _url_id(url: str) -> str:
        return base64.urlsafe_b64encode(url.encode()).decode().strip("=")

    def _headers(self):
        return {"x-apikey": self.api_key or ""}

    async def lookup(self, ioc: str, ioc_type: str) -> dict:
        if not self.api_key:
            return {"available": False, "error": "VirusTotal API key not configured"}

        if ioc_type in {"MD5", "SHA1", "SHA256"}:
            path = f"/files/{ioc}"
        elif ioc_type == "IP":
            path = f"/ip_addresses/{ioc}"
        elif ioc_type == "DOMAIN":
            path = f"/domains/{ioc}"
        elif ioc_type == "URL":
            path = f"/urls/{self._url_id(ioc)}"
        else:
            return {"available": False, "error": "Unsupported IOC type for VirusTotal"}

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(f"{self.BASE_URL}{path}", headers=self._headers())

        if resp.status_code == 404:
            return {"available": True, "found": False, "stats": {}, "raw": {}}
        if resp.status_code == 429:
            return {"available": False, "error": "VirusTotal rate limit exceeded"}
        if resp.status_code >= 400:
            return {"available": False, "error": f"VirusTotal error {resp.status_code}: {resp.text[:300]}"}

        payload = resp.json()
        attrs = payload.get("data", {}).get("attributes", {})
        stats = attrs.get("last_analysis_stats", {}) or {}
        return {
            "available": True,
            "found": True,
            "stats": {
                "malicious": int(stats.get("malicious", 0) or 0),
                "suspicious": int(stats.get("suspicious", 0) or 0),
                "harmless": int(stats.get("harmless", 0) or 0),
                "undetected": int(stats.get("undetected", 0) or 0),
            },
            "reputation": attrs.get("reputation"),
            "tags": attrs.get("tags", []),
            "last_analysis_date": attrs.get("last_analysis_date"),
        }
