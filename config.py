import re

SEP = "-" * 50

URL_PATTERN = re.compile(
    r"^"
    r"(?:(?P<scheme>[a-zA-Z][a-zA-Z0-9+\-.]*)://)?"
    r"(?P<host>"
    r"(?:\[(?P<ipv6>[0-9a-fA-F:]+)\])"
    r"|"
    r"(?P<domain>(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,})"
    r")"
    r"(?::(?P<port>\d{1,5}))?"
    r"(?P<path>/[^\s?#]*)?"
    r"(?:\?(?P<query>[^\s#]*))?"
    r"(?:#(?P<fragment>[^\s]*))?"
    r"$"
)
