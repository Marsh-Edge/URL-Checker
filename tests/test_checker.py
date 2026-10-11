import sys
sys.path.insert(0, ".")

from checker import connectivity


class DummyResp:
    def __init__(self, status_code=200, success=True, redirect=False):
        self.status_code = status_code
        self.is_success = success
        self.is_redirect = redirect


class DummyClient:
    def __init__(self, resp=None, exc=None):
        self.resp = resp
        self.exc = exc

    def head(self, url):
        if self.exc:
            raise self.exc
        return self.resp


def test_reachable_ok():
    c = connectivity("http://x", client=DummyClient(DummyResp(200)))
    assert c["reachable"] is True
    assert c["status"] == 200
    assert c["error"] is None


def test_redirect_ok():
    c = connectivity("http://x", client=DummyClient(DummyResp(301, success=False, redirect=True)))
    assert c["reachable"] is True
    assert c["status"] == 301


def test_http_error():
    c = connectivity("http://x", client=DummyClient(DummyResp(500, success=False, redirect=False)))
    assert c["reachable"] is False
    assert c["status"] == 500
    assert c["error"] is not None


def test_timeout():
    import httpx
    c = connectivity("http://x", client=DummyClient(exc=httpx.TimeoutException("t")))
    assert c["reachable"] is False
    assert c["status"] is None
    assert "timeout" in c["error"].lower()


def test_connect_error():
    import httpx
    c = connectivity("http://x", client=DummyClient(exc=httpx.ConnectError("c")))
    assert c["reachable"] is False
    assert c["status"] is None
    assert "connect" in c["error"].lower()
