import requests

FIELD_LABELS = {
    "query": "IP Address",
    "continent": "Continent",
    "continentCode": "Continent Code",
    "country": "Country",
    "countryCode": "Country Code",
    "region": "Region Code",
    "regionName": "Region",
    "district": "District",
    "city": "City",
    "zip": "ZIP Code",
    "lat": "Latitude",
    "lon": "Longitude",
    "timezone": "Timezone",
    "offset": "UTC Offset",
    "currency": "Currency",
    "isp": "ISP",
    "org": "Organization",
    "as": "ASN",
    "asname": "AS Name",
    "reverse": "Reverse DNS",
    "mobile": "Mobile Connection",
    "proxy": "Proxy / VPN / Tor",
    "hosting": "Hosting / Datacenter",
}

FIELD_ORDER = [
    "query",
    "continent",
    "continentCode",
    "country",
    "countryCode",
    "regionName",
    "region",
    "district",
    "city",
    "zip",
    "lat",
    "lon",
    "timezone",
    "offset",
    "currency",
    "isp",
    "org",
    "as",
    "asname",
    "reverse",
    "mobile",
    "proxy",
    "hosting",
]


def ip_lookup(query: str) -> dict:
    query = query.strip()

    if not query:
        raise ValueError("Empty query")

    fields = ",".join([
        "status",
        "message",
        "query",
        "continent",
        "continentCode",
        "country",
        "countryCode",
        "region",
        "regionName",
        "district",
        "city",
        "zip",
        "lat",
        "lon",
        "timezone",
        "offset",
        "currency",
        "isp",
        "org",
        "as",
        "asname",
        "reverse",
        "mobile",
        "proxy",
        "hosting",
    ])

    response = requests.get(
        f"http://ip-api.com/json/{query}",
        params={"fields": fields},
        timeout=6,
    )

    response.raise_for_status()

    data = response.json()

    if data.get("status") == "fail":
        raise ValueError(data.get("message", "Lookup failed"))

    result = []

    for key in FIELD_ORDER:
        value = data.get(key)

        if value is None or value == "":
            continue

        if isinstance(value, bool):
            value = "Yes" if value else "No"

        result.append({
            "label": FIELD_LABELS.get(key, key),
            "value": value,
        })

    return {
        "fields": result
    }