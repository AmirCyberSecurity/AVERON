import socket
import requests

from core.lookups.ip_lookup import ip_lookup


FIELD_LABELS = {
    "domain": "Domain",
    "ip": "IP Address",
    "asn": "ASN",
    "asname": "AS Name",
    "country": "Server Country",
    "city": "Server City",
    "reverse": "Reverse DNS",
    "waf": "WAF / CDN",
    "http_status": "HTTP Status",
    "https": "HTTPS",
    "server": "Web Server",
    "powered_by": "Powered By",
    "content_type": "Content Type",
    "redirect": "Redirect",
}


FIELD_ORDER = [
    "domain",
    "ip",
    "asn",
    "asname",
    "country",
    "city",
    "reverse",
    "waf",
    "http_status",
    "https",
    "server",
    "powered_by",
    "content_type",
    "redirect",
]


CLOUDFLARE_ASNS = {
    "AS13335",
}


def clean_domain(query: str) -> str:
    query = query.strip().lower()

    if not query:
        raise ValueError("Empty query")

    query = query.removeprefix("https://")
    query = query.removeprefix("http://")
    query = query.removeprefix("www.")

    query = query.split("/")[0]
    query = query.split("?")[0]
    query = query.split("#")[0]
    query = query.split(":")[0]

    if not query:
        raise ValueError("Invalid domain")

    return query


def resolve_ip(domain: str) -> str:
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        raise ValueError("Domain could not be resolved")


def get_reverse_dns(ip: str) -> str:
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except (socket.herror, socket.gaierror):
        return ""


def get_http_info(domain: str) -> dict:
    result = {
        "http_status": "",
        "https": "",
        "server": "",
        "powered_by": "",
        "content_type": "",
        "redirect": "",
        "waf": "",
    }

    headers = {
        "User-Agent": "AVERON/1.0",
        "Accept": "*/*",
    }

    try:
        response = requests.get(
            f"https://{domain}",
            headers=headers,
            timeout=6,
            allow_redirects=True,
        )

        result["http_status"] = str(response.status_code)
        result["https"] = "Yes"

        server = response.headers.get("Server")
        powered_by = response.headers.get("X-Powered-By")
        content_type = response.headers.get("Content-Type")

        if server:
            result["server"] = server

        if powered_by:
            result["powered_by"] = powered_by

        if content_type:
            result["content_type"] = content_type

        if response.url != f"https://{domain}":
            result["redirect"] = response.url

        result["waf"] = detect_waf(
            response.headers,
            response.text[:50000],
        )

        return result

    except requests.RequestException:
        pass

    try:
        response = requests.get(
            f"http://{domain}",
            headers=headers,
            timeout=6,
            allow_redirects=True,
        )

        result["http_status"] = str(response.status_code)
        result["https"] = "No"

        server = response.headers.get("Server")
        powered_by = response.headers.get("X-Powered-By")
        content_type = response.headers.get("Content-Type")

        if server:
            result["server"] = server

        if powered_by:
            result["powered_by"] = powered_by

        if content_type:
            result["content_type"] = content_type

        if response.url != f"http://{domain}":
            result["redirect"] = response.url

        result["waf"] = detect_waf(
            response.headers,
            response.text[:50000],
        )

    except requests.RequestException:
        pass

    return result


def detect_waf(headers, body: str) -> str:
    header_data = " ".join(
        f"{key}: {value}"
        for key, value in headers.items()
    ).lower()

    body_data = body.lower()

    if (
        "cf-ray" in header_data
        or "cloudflare" in header_data
        or "cloudflare" in body_data
    ):
        return "Cloudflare"

    if (
        "x-sucuri-id" in header_data
        or "sucuri" in header_data
        or "sucuri" in body_data
    ):
        return "Sucuri"

    if (
        "x-cdn" in header_data
        and "incapsula" in header_data
    ):
        return "Imperva Incapsula"

    if (
        "incap_ses" in header_data
        or "visid_incap" in header_data
        or "incapsula" in header_data
    ):
        return "Imperva Incapsula"

    if "akamai" in header_data:
        return "Akamai"

    if "fastly" in header_data:
        return "Fastly"

    if "x-amzn-" in header_data:
        return "Amazon AWS"

    if "azure" in header_data:
        return "Microsoft Azure"

    return ""


def domain_lookup(query: str) -> dict:
    domain = clean_domain(query)

    ip = resolve_ip(domain)

    ip_data = ip_lookup(ip)

    ip_fields = {
        field["label"]: field["value"]
        for field in ip_data.get("fields", [])
    }

    asn = ip_fields.get("ASN")
    asname = ip_fields.get("AS Name")

    waf = ""

    if asn in CLOUDFLARE_ASNS:
        waf = "Cloudflare"

    http_data = get_http_info(domain)

    if http_data.get("waf"):
        waf = http_data["waf"]

    data = {
        "domain": domain,
        "ip": ip,
        "asn": asn,
        "asname": asname,
        "country": ip_fields.get("Country"),
        "city": ip_fields.get("City"),
        "reverse": ip_fields.get("Reverse DNS"),
        "waf": waf,
        "http_status": http_data.get("http_status"),
        "https": http_data.get("https"),
        "server": http_data.get("server"),
        "powered_by": http_data.get("powered_by"),
        "content_type": http_data.get("content_type"),
        "redirect": http_data.get("redirect"),
    }

    result = []

    for key in FIELD_ORDER:
        value = data.get(key)

        if value is None or value == "":
            continue

        result.append({
            "label": FIELD_LABELS.get(key, key),
            "value": value,
        })

    return {
        "fields": result
    }