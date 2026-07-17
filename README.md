<div align="center">

# URL-Checker

**A lightweight Python CLI tool that validates URL format and checks server reachability.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg)](https://www.python.org/)
[![httpx](https://img.shields.io/badge/HTTP Client-httpx-009688.svg)](https://www.python-httpx.org/)

</div>

---

## Table of Contents

- [About the Project](#about-the-project)
- [Why This Project?](#why-this-project)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)
- [Acknowledgments](#acknowledgments)
- [FAQ](#faq)

---

## About the Project

URL-Checker is a command-line utility that performs two core operations on any given URL:

1. **Format Validation** -- Parses and validates the URL against a comprehensive regex pattern, ensuring it uses a supported scheme (`http` or `https`), contains a valid hostname, and follows standard URL syntax.
2. **Connectivity Check** -- Sends an HTTP `HEAD` request to the validated URL and reports the server's response status and response time.

The tool is designed for quick, offline URL diagnostics without relying on web interfaces or external services.

---

## Why This Project?

When working with URLs in development, scripting, or monitoring workflows, you often need a fast way to answer two questions:

- *Is this URL syntactically valid?*
- *Is the server behind this URL actually reachable?*

URL-Checker combines both checks into a single, lightweight CLI invocation. It parses URLs with named regex groups (scheme, host, port, path, query, fragment) and uses `httpx` for reliable HTTP connectivity testing with redirect following and configurable timeouts.

---

## Features

| Feature | Description |
|---------|-------------|
| **URL Format Validation** | Regex-based parsing with named capture groups for scheme, host, port, path, query, and fragment |
| **HTTP/HTTPS Support** | Validates and tests URLs using both `http://` and `https://` schemes |
| **IPv6 Support** | Recognizes IPv6 addresses enclosed in brackets (e.g., `[::1]`) |
| **Domain Name Validation** | Supports standard domain names with subdomains and TLDs |
| **Port Detection** | Parses and validates port numbers (1--65535 range) |
| **HTTP HEAD Request** | Uses lightweight `HEAD` requests to check reachability without downloading content |
| **Redirect Following** | Automatically follows HTTP redirects |
| **Response Time Measurement** | Reports server response time in milliseconds |
| **Timeout Handling** | Configurable request timeout (default: 10 seconds) |
| **Detailed Error Reporting** | Clear, descriptive error messages for each failure type |
| **Custom User-Agent** | Identifies requests with `URL-Checker/1.0` User-Agent header |

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| [Python](https://www.python.org/) | Primary language |
| [httpx](https://www.python-httpx.org/) | Async-capable HTTP client for connectivity checks |
| `re` (stdlib) | Regular expression engine for URL parsing |
| `time` (stdlib) | High-resolution timing via `time.monotonic()` |

---

## Project Structure

```
URL-Checker/
├── app.py          # Entry point -- orchestrates validation and connectivity check
├── config.py       # Constants and compiled URL regex pattern
├── validator.py    # URL format validation logic
├── checker.py      # HTTP connectivity check via httpx
├── LICENSE         # MIT License
└── README.md       # This file
```

---

## Installation

### Prerequisites

- Python 3.10 or higher
- `pip` (Python package manager)

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/Marsh-Edge/URL-Checker.git
   cd URL-Checker
   ```

2. **Install the dependency**

   ```bash
   pip install httpx
   ```

3. **Verify installation**

   ```bash
   python app.py
   ```

---

## Usage

Run the tool from the project directory:

```bash
python app.py
```

You will be prompted to enter a URL. The tool will validate its format and then test connectivity.

### Example -- Valid URL

```
Enter URL to check: https://www.example.com

--------------------------------------------------
[*] Validating URL format... OK
[*] Hostname: www.example.com
[*] Connecting to server... OK
[*] Server responded: 200
[*] Response time: 142 ms
--------------------------------------------------
Result: VALID and REACHABLE (200 - 142ms)
```

### Example -- Invalid URL

```
Enter URL to check: not-a-url

--------------------------------------------------
[*] Validating URL format... FAILED
[!] Error: URL must include a scheme (http:// or https://)
--------------------------------------------------
```

### Example -- Unreachable Server

```
Enter URL to check: https://this-server-does-not-exist.invalid

--------------------------------------------------
[*] Validating URL format... OK
[*] Hostname: this-server-does-not-exist.invalid
[*] Connecting to server... FAILED
[!] Error: Connection failed: ...
--------------------------------------------------
Result: FAILED
```

---

## Roadmap

### Completed

- [x] URL format validation via regex
- [x] HTTP/HTTPS scheme support
- [x] IPv6 address recognition
- [x] Domain name and port parsing
- [x] HTTP connectivity check with `httpx`
- [x] Response time measurement
- [x] Redirect following
- [x] Timeout and error handling

### Planned

- [ ] Machine learning-based URL classification (phishing / malicious detection)
- [ ] Batch URL checking from file input
- [ ] JSON output mode for scripting and automation
- [ ] DNS resolution check
- [ ] SSL certificate validation
- [ ] `requirements.txt` or `pyproject.toml` for dependency management

---

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add your feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

Please ensure your code follows the existing style and includes clear commit messages.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Marsh
```

---

## Author

**Marsh** -- [GitHub Profile](https://github.com/Marsh-Edge)

---

## Acknowledgments

- [httpx](https://www.python-httpx.org/) -- A next-generation HTTP client for Python
- [Python](https://www.python.org/) -- The programming language
- Inspired by the need for a simple, scriptable URL validation and reachability tool

---

## FAQ

<details>
<summary><strong>Does this tool support FTP or other protocols?</strong></summary>

No. URL-Checker currently only supports `http://` and `https://` schemes. Other protocols are rejected during validation.
</details>

<details>
<summary><strong>What happens if the server returns a redirect?</strong></summary>

The tool follows redirects automatically. The final response status code and time are reported.
</details>

<details>
<summary><strong>Can I use this in a script or automation pipeline?</strong></summary>

Not yet. The current version is interactive (reads from `stdin`). A JSON output mode for non-interactive use is planned in the [Roadmap](#roadmap).
</details>

---

<div align="center">

Made with Python

</div>
