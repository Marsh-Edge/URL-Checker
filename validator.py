from config import URL_PATTERN


def validate(url: str) -> dict:
    if not url or not url.strip():
        return {"valid": False, "error": "URL is empty"}

    m = URL_PATTERN.match(url.strip())
    if not m:
        return {"valid": False, "error": "URL format is invalid"}

    scheme = m.group("scheme")
    if not scheme:
        return {"valid": False, "error": "URL must include a scheme (http:// or https://)"}
    if scheme.lower() not in ("http", "https"):
        return {"valid": False, "error": f"Unsupported scheme '{scheme}' (use http or https)"}
    if not m.group("host"):
        return {"valid": False, "error": "No hostname found"}

    return {"valid": True, "scheme": scheme.lower(), "hostname": m.group("host")}
