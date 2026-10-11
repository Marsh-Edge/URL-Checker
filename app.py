import argparse
import json
import sys

from validator import validate
from checker import connectivity
from config import SEP, __version__


def _normalize(url: str) -> str:
    u = url.strip()
    if not u:
        return u
    low = u.lower()
    if low.startswith(("http://", "https://")):
        return u
    if "://" in u:
        return u
    return f"https://{u}"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validate URL format and check server reachability")
    parser.add_argument("url", nargs="?", help="URL to check (if omitted, runs interactively)")
    parser.add_argument("-t", "--timeout", type=int, default=10, help="Request timeout in seconds (default: 10)")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    parser.add_argument("--quiet", action="store_true", help="Minimal output")
    parser.add_argument("--version", action="version", version=f"URL-Checker {__version__}")
    args = parser.parse_args(argv)

    interactive = args.url is None

    try:
        if interactive:
            try:
                url_in = input("Enter URL to check: ").strip()
            except EOFError:
                return 1
            print()
            if not args.quiet:
                print(SEP)
        else:
            url_in = args.url.strip() if args.url else ""

        if not url_in:
            v = {"valid": False, "error": "URL is empty", "scheme": None, "hostname": None, "port": None}
            c = {"reachable": False, "status": None, "ms": None, "error": v["error"]}
        else:
            v = validate(url_in)
            if v["valid"]:
                url_check = _normalize(url_in)
                c = connectivity(url_check, timeout=args.timeout)
            else:
                c = {"reachable": False, "status": None, "ms": None, "error": v["error"]}

        result = {
            "url_input": url_in,
            "normalized_url": _normalize(url_in) if url_in else None,
            "valid": v["valid"],
            "scheme": v["scheme"],
            "hostname": v["hostname"],
            "port": v["port"],
            "reachable": c["reachable"],
            "status": c["status"],
            "response_ms": c["ms"],
            "error": c["error"] if c["error"] else v["error"] if not v["valid"] else None,
        }

        if args.json:
            print(json.dumps(result, indent=2))
            return 0 if (result["valid"] and result["reachable"]) else 1

        if not args.quiet:
            if interactive:
                print("[*] Validating URL format...", end=" ", flush=True)
                if result["valid"]:
                    print("OK")
                    print(f"[*] Hostname: {result['hostname']}")
                    print("[*] Connecting to server...", end=" ", flush=True)
                    if result["reachable"]:
                        print("OK")
                        print(f"[*] Server responded: {result['status']}")
                        if result["response_ms"] is not None:
                            print(f"[*] Response time: {result['response_ms']:.0f} ms")
                        print(SEP)
                        print(f"Result: VALID and REACHABLE ({result['status']} - {result['response_ms']:.0f}ms)" if result["status"] is not None and result["response_ms"] is not None else "Result: VALID and REACHABLE")
                    else:
                        print("FAILED")
                        print(f"[!] Error: {result['error'] or c['error']}")
                        print(SEP)
                        print("Result: FAILED")
                else:
                    print("FAILED")
                    print(f"[!] Error: {result['error']}")
                    print(SEP)
            else:
                if result["valid"] and result["reachable"]:
                    if result["status"] is not None and result["response_ms"] is not None:
                        print(f"OK {result['status']} {result['response_ms']:.0f}ms {result['normalized_url']}")
                    else:
                        print(f"OK {result['normalized_url']}")
                elif not result["valid"]:
                    print(f"INVALID {result['error']}", file=sys.stderr)
                else:
                    print(f"UNREACHABLE {result['error']}", file=sys.stderr)

        if interactive and not args.quiet and args.url is None:
            print()
            try:
                input("Press Enter to exit...")
            except EOFError:
                pass

        if result["valid"] and result["reachable"]:
            return 0
        return 1
    except KeyboardInterrupt:
        if not args.quiet:
            print()
        return 130


if __name__ == "__main__":
    sys.exit(main())
