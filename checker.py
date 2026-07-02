import time

import httpx


def connectivity(url: str, timeout: int = 10) -> dict:
    start = time.monotonic()
    try:
        with httpx.Client(follow_redirects=True, timeout=timeout,
                          headers={"User-Agent": "URL-Checker/1.0"}) as c:
            r = c.head(url)
            ms = round((time.monotonic() - start) * 1000, 2)
            if r.is_success or r.is_redirect:
                return {"reachable": True, "status": r.status_code, "ms": ms}
            return {"reachable": False, "error": f"HTTP {r.status_code}"}
    except httpx.TimeoutException:
        return {"reachable": False, "error": "Request timed out"}
    except httpx.ConnectError as e:
        return {"reachable": False, "error": f"Connection failed: {e}"}
    except Exception as e:
        return {"reachable": False, "error": str(e)}
