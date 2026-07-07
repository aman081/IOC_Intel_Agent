def verdict_from_score(score: int) -> str:
    if score >= 81:
        return "Critical"
    if score >= 51:
        return "Malicious"
    if score >= 21:
        return "Suspicious"
    return "Clean"


def recommendation_from_verdict(verdict: str) -> str:
    return {
        "Critical": "Block immediately, hunt across logs, and escalate for incident response.",
        "Malicious": "Block or quarantine, investigate affected assets, and add to watchlist.",
        "Suspicious": "Monitor, validate context, and investigate if seen in internal telemetry.",
        "Clean": "No immediate action required; continue normal monitoring.",
    }.get(verdict, "Review manually.")


def score_ioc(ioc_type: str, vt: dict | None, abuse: dict | None) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []

    vt = vt or {}
    abuse = abuse or {}

    if vt.get("available") and vt.get("found", True):
        stats = vt.get("stats", {}) or {}
        malicious = int(stats.get("malicious", 0) or 0)
        suspicious = int(stats.get("suspicious", 0) or 0)

        if ioc_type == "IP":
            if malicious > 10:
                score += 40
                reasons.append(f"VirusTotal shows high malicious detections: {malicious}.")
            elif malicious > 5:
                score += 25
                reasons.append(f"VirusTotal shows multiple malicious detections: {malicious}.")
            elif malicious > 0:
                score += 15
                reasons.append(f"VirusTotal shows some malicious detections: {malicious}.")
        elif ioc_type in {"DOMAIN", "URL"}:
            if malicious > 10:
                score += 50
                reasons.append(f"VirusTotal shows high malicious detections: {malicious}.")
            elif malicious > 5:
                score += 35
                reasons.append(f"VirusTotal shows multiple malicious detections: {malicious}.")
            elif malicious > 0:
                score += 20
                reasons.append(f"VirusTotal shows some malicious detections: {malicious}.")
        elif ioc_type in {"MD5", "SHA1", "SHA256"}:
            if malicious > 20:
                score += 60
                reasons.append(f"VirusTotal file reputation has very high malicious detections: {malicious}.")
            elif malicious > 10:
                score += 40
                reasons.append(f"VirusTotal file reputation has high malicious detections: {malicious}.")
            elif malicious > 0:
                score += 25
                reasons.append(f"VirusTotal file reputation has malicious detections: {malicious}.")

        if suspicious > 0:
            score += 10
            reasons.append(f"VirusTotal also has suspicious detections: {suspicious}.")
    elif vt.get("error"):
        reasons.append(f"VirusTotal not used: {vt.get('error')}.")
    elif vt.get("available") and not vt.get("found", True):
        reasons.append("VirusTotal did not find an existing report for this IOC.")

    if ioc_type == "IP":
        if abuse.get("available"):
            abuse_score = int(abuse.get("abuse_confidence_score", 0) or 0)
            if abuse_score >= 90:
                score += 40
                reasons.append(f"AbuseIPDB abuse confidence is very high: {abuse_score}.")
            elif abuse_score >= 70:
                score += 25
                reasons.append(f"AbuseIPDB abuse confidence is high: {abuse_score}.")
            elif abuse_score >= 25:
                score += 10
                reasons.append(f"AbuseIPDB abuse confidence is notable: {abuse_score}.")

            if int(abuse.get("total_reports", 0) or 0) > 0:
                score += 5
                reasons.append(f"AbuseIPDB reports found: {abuse.get('total_reports')}.")
            if abuse.get("is_tor"):
                score += 10
                reasons.append("AbuseIPDB indicates this IP is associated with Tor.")
        elif abuse.get("error"):
            reasons.append(f"AbuseIPDB not used: {abuse.get('error')}.")

    score = max(0, min(100, score))
    if not reasons:
        reasons.append("No strong malicious signal was found from the configured sources.")
    return score, reasons
