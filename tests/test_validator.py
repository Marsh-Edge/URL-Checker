import sys
sys.path.insert(0, ".")

from validator import validate


def test_empty():
    r = validate("")
    assert r["valid"] is False
    assert "empty" in r["error"].lower()


def test_no_scheme():
    r = validate("example.com")
    assert r["valid"] is False


def test_invalid_scheme():
    r = validate("ftp://example.com")
    assert r["valid"] is False
    assert "scheme" in r["error"].lower()


def test_valid_http():
    r = validate("http://example.com")
    assert r["valid"] is True
    assert r["scheme"] == "http"
    assert r["hostname"] == "example.com"


def test_valid_https():
    r = validate("https://www.example.com")
    assert r["valid"] is True
    assert r["scheme"] == "https"


def test_ipv6():
    r = validate("http://[2001:db8::1]")
    assert r["valid"] is True


def test_subdomain_path_query_frag():
    r = validate("https://api.example.com/path?q=1#top")
    assert r["valid"] is True
    assert r["hostname"] == "api.example.com"


def test_port_ok():
    r = validate("http://example.com:80")
    assert r["valid"] is True
    assert r["port"] == 80


def test_port_max():
    r = validate("http://example.com:65535")
    assert r["valid"] is True
    assert r["port"] == 65535


def test_port_zero():
    r = validate("http://example.com:0")
    assert r["valid"] is False


def test_port_too_high():
    r = validate("http://example.com:65536")
    assert r["valid"] is False
