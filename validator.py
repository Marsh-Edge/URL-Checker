from config import URL_PATTERN


def validate(url: str) -> dict:
    if not url or not url.strip():
        return {"valid": False, "error": "URL is empty", "scheme": None, "hostname": None, "port": None}

    s = url.strip()
    m = URL_PATTERN.match(s)
    if not m:
        return {"valid": False, "error": "URL format is invalid", "scheme": None, "hostname": None, "port": None}

    scheme = m.group("scheme")
    if not scheme:
        return {"valid": False, "error": "URL must include a scheme (http:// or https://)", "scheme": None, "hostname": None, "port": None}
    if scheme.lower() not in ("http", "https"):
        return {"valid": False, "error": f"Unsupported scheme '{scheme}' (use http or https)", "scheme": scheme.lower(), "hostname": m.group("host"), "port": None}
    if not m.group("host"):
        return {"valid": False, "error": "No hostname found", "scheme": scheme.lower(), "hostname": None, "port": None}

    port = m.group("port")
    if port is not None:
        try:
            p = int(port)
        except ValueError:
            return {"valid": False, "error": "Invalid port number", "scheme": scheme.lower(), "hostname": m.group("host"), "port": None}
        if p < 1 or p > 65535:
            return {"valid": False, "error": f"Invalid port number '{p}' (must be 1-65535)", "scheme": scheme.lower(), "hostname": m.group("host"), "port": p}

    return {"valid": True, "scheme": scheme.lower(), "hostname": m.group("host"), "port": p if port is not None else None}
