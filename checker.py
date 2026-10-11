import time

import httpx

from config import __version__


def connectivity(url: str, timeout: int = 10, *, client=None) -> dict:
    start = time.monotonic()
    ua = f"URL-Checker/{__version__}"
    try:
        if client is not None:
            r = client.head(url)
            ms = round((time.monotonic() - start) * 1000, 2)
            if getattr(r, "is_success", False) or getattr(r, "is_redirect", False):
                return {"reachable": True, "status": getattr(r, "status_code", None), "ms": ms, "error": None}
            return {"reachable": False, "status": getattr(r, "status_code", None), "ms": ms, "error": f"HTTP {getattr(r, 'status_code', 'unknown')}"}
        with httpx.Client(follow_redirects=True, timeout=timeout,
                          headers={"User-Agent": ua}) as c:
            r = c.head(url)
            ms = round((time.monotonic() - start) * 1000, 2)
            if r.is_success or r.is_redirect:
                return {"reachable": True, "status": r.status_code, "ms": ms, "error": None}
            return {"reachable": False, "status": r.status_code, "ms": ms, "error": f"HTTP {r.status_code}"}
    except httpx.TimeoutException:
        ms = round((time.monotonic() - start) * 1000, 2)
        return {"reachable": False, "status": None, "ms": ms, "error": "Request timed out (timeout)"}
    except httpx.ConnectError as e:
        ms = round((time.monotonic() - start) * 1000, 2)
        return {"reachable": False, "status": None, "ms": ms, "error": f"Connection failed: {e}"}
    except Exception as e:
        ms = round((time.monotonic() - start) * 1000, 2)
        return {"reachable": False, "status": None, "ms": ms, "error": str(e)}
