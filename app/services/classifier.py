import ipaddress
import re
from urllib.parse import urlparse

HEX_RE = re.compile(r"^[a-fA-F0-9]+$")
DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?!-)([A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,63}$"
)


def normalize_ioc(value: str) -> str:
    v = value.strip()
    v = v.replace("hxxp://", "http://").replace("hxxps://", "https://")
    v = v.replace("[.]", ".").replace("(.)", ".")
    return v.strip()


def classify_ioc(value: str) -> str:
    v = normalize_ioc(value)

    try:
        ipaddress.ip_address(v)
        return "IP"
    except ValueError:
        pass

    parsed = urlparse(v)
    if parsed.scheme in {"http", "https"} and parsed.netloc:
        return "URL"

    if HEX_RE.match(v):
        if len(v) == 32:
            return "MD5"
        if len(v) == 40:
            return "SHA1"
        if len(v) == 64:
            return "SHA256"

    if DOMAIN_RE.match(v.lower()):
        return "DOMAIN"

    return "UNKNOWN"
