from validator import validate
from checker import connectivity
from config import SEP


def main() -> None:
    url = input("Enter URL to check: ").strip()
    print()
    print(SEP)

    print("[*] Validating URL format...", end=" ", flush=True)
    v = validate(url)
    if not v["valid"]:
        print("FAILED")
        print(f"[!] Error: {v['error']}")
        print(SEP)
    else:
        print("OK")
        print(f"[*] Hostname: {v['hostname']}")

        print("[*] Connecting to server...", end=" ", flush=True)
        c = connectivity(url)
        if c["reachable"]:
            print("OK")
            print(f"[*] Server responded: {c['status']}")
            print(f"[*] Response time: {c['ms']:.0f} ms")
            print(SEP)
            print(f"Result: VALID and REACHABLE ({c['status']} - {c['ms']:.0f}ms)")
        else:
            print("FAILED")
            print(f"[!] Error: {c['error']}")
            print(SEP)
            print("Result: FAILED")

    print()
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
