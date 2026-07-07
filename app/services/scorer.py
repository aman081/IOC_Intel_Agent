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
        "Critical":
            "Block immediately, hunt across logs, and escalate for incident response.",

        "Malicious":
            "Block or quarantine, investigate affected assets, and add to watchlist.",

        "Suspicious":
            "Monitor, validate context, and investigate if seen in internal telemetry.",

        "Clean":
            "No immediate action required. Its clean. Continue normal monitoring.",
    }.get(
        verdict,
        "Review manually."
    )


def score_ioc(
    ioc_type: str,
    vt: dict | None,
    abuse: dict | None
) -> tuple[int, list[str]]:

    score = 0

    reasons: list[str] = []

    vt = vt or {}
    abuse = abuse or {}

    tags = vt.get("tags", [])

    reputation = vt.get("reputation", 0)

    # ======================================================
    # VIRUSTOTAL SCORING
    # ======================================================

    if vt.get("available") and vt.get("found", True):

        stats = vt.get("stats", {}) or {}

        malicious = int(
            stats.get("malicious", 0) or 0
        )

        suspicious = int(
            stats.get("suspicious", 0) or 0
        )

        # ------------------------------------
        # FILE HASHES
        # ------------------------------------

        if ioc_type in {
            "MD5",
            "SHA1",
            "SHA256"
        }:

            if malicious >= 50:

                score += 80

                reasons.append(
                    f"VirusTotal reports extremely high detections ({malicious})."
                )

            elif malicious >= 20:

                score += 60

                reasons.append(
                    f"VirusTotal reports high detections ({malicious})."
                )

            elif malicious >= 10:

                score += 40

                reasons.append(
                    f"VirusTotal reports several detections ({malicious})."
                )

            elif malicious > 0:

                score += 20

                reasons.append(
                    f"VirusTotal reports some detections ({malicious})."
                )

        # ------------------------------------
        # DOMAINS / URLS
        # ------------------------------------

        elif ioc_type in {
            "DOMAIN",
            "URL"
        }:

            if malicious >= 20:

                score += 70

            elif malicious >= 10:

                score += 50

            elif malicious > 0:

                score += 25

            if malicious > 0:

                reasons.append(
                    f"VirusTotal reports {malicious} malicious detections."
                )

        # ------------------------------------
        # IP ADDRESSES
        # ------------------------------------

        elif ioc_type == "IP":

            if malicious >= 20:

                score += 60

            elif malicious >= 10:

                score += 40

            elif malicious > 0:

                score += 20

            if malicious > 0:

                reasons.append(
                    f"VirusTotal reports {malicious} malicious detections."
                )

        # ------------------------------------
        # SUSPICIOUS ENGINES
        # ------------------------------------

        if suspicious > 0:

            suspicious_points = min(
                suspicious * 2,
                10
            )

            score += suspicious_points

            reasons.append(
                f"VirusTotal reports {suspicious} suspicious detections."
            )

        # ------------------------------------
        # REPUTATION
        # ------------------------------------

        if reputation < -500:

            score += 40

            reasons.append(
                f"Very poor VirusTotal reputation ({reputation})."
            )

        elif reputation < -100:

            score += 20

            reasons.append(
                f"Negative VirusTotal reputation ({reputation})."
            )

        elif reputation > 500:

            score -= 15

            reasons.append(
                f"Strong positive VirusTotal reputation ({reputation})."
            )

        elif reputation > 100:

            score -= 10

            reasons.append(
                f"Positive VirusTotal reputation ({reputation})."
            )

        # ------------------------------------
        # TAG SCORING
        # ------------------------------------

        tag_scores = {
            "via-tor": 10,
            "powershell": 15,
            "known-distributor": 15,
            "detect-debug-environment": 10,
            "ransomware": 40,
            "trojan": 30,
            "phishing": 30,
            "backdoor": 30,
            "credential-theft": 30
        }

        for tag in tags:

            if tag in tag_scores:

                score += tag_scores[tag]

                reasons.append(
                    f"High-risk tag detected: {tag}"
                )

    elif vt.get("error"):

        reasons.append(
            f"VirusTotal not used: {vt.get('error')}."
        )

    elif vt.get("available") and not vt.get("found", True):

        reasons.append(
            "VirusTotal did not find an existing report for this IOC."
        )

    # ======================================================
    # ABUSEIPDB SCORING
    # ======================================================

    if ioc_type == "IP":

        if abuse.get("available"):

            abuse_score = int(
                abuse.get(
                    "abuse_confidence_score",
                    0
                ) or 0
            )

            if abuse_score >= 90:

                score += 50

                reasons.append(
                    f"AbuseIPDB confidence is extremely high ({abuse_score})."
                )

            elif abuse_score >= 70:

                score += 35

                reasons.append(
                    f"AbuseIPDB confidence is high ({abuse_score})."
                )

            elif abuse_score >= 40:

                score += 20

                reasons.append(
                    f"AbuseIPDB confidence is elevated ({abuse_score})."
                )

            elif abuse_score >= 20:

                score += 10

                reasons.append(
                    f"AbuseIPDB confidence is notable ({abuse_score})."
                )

            if abuse.get("is_tor"):

                score += 15

                reasons.append(
                    "AbuseIPDB indicates TOR usage."
                )

        elif abuse.get("error"):

            reasons.append(
                f"AbuseIPDB not used: {abuse.get('error')}."
            )

    # ======================================================
    # FINAL NORMALIZATION
    # ======================================================

    score = max(
        0,
        min(100, score)
    )

    if not reasons:

        reasons.append(
            "No strong malicious signal was found from the configured sources."
        )

    return score, reasons
