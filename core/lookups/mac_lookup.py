import re
import requests


FIELD_LABELS = {
    "mac": "MAC Address",
    "oui": "OUI",
    "vendor": "Vendor",
    "address_type": "Address Type",
    "assignment": "Assignment",
    "transmission": "Transmission Type",
    "oui_prefix": "OUI Prefix",
    "device_identifier": "Device Identifier",
}


FIELD_ORDER = [
    "mac",
    "oui",
    "vendor",
    "address_type",
    "assignment",
    "transmission",
    "oui_prefix",
    "device_identifier",
]


def normalize_mac(query: str) -> str:
    query = query.strip()

    mac = re.sub(r"[^0-9a-fA-F]", "", query)

    if len(mac) != 12:
        raise ValueError("Invalid MAC address length.")

    if not re.fullmatch(r"[0-9a-fA-F]{12}", mac):
        raise ValueError("Invalid MAC address.")

    return mac.upper()


def format_mac(mac: str) -> str:
    return ":".join(
        mac[i:i + 2]
        for i in range(0, 12, 2)
    )


def get_vendor(mac: str) -> str:
    try:
        response = requests.get(
            f"https://api.macvendors.com/{mac}",
            timeout=6,
        )
    except requests.RequestException:
        return ""

    if response.status_code == 404:
        return ""

    response.raise_for_status()

    return response.text.strip()


def mac_lookup(query: str) -> dict:
    mac = normalize_mac(query)

    formatted_mac = format_mac(mac)
    oui = mac[:6]

    first_octet = int(mac[:2], 16)

    is_multicast = bool(first_octet & 0x01)
    is_local = bool(first_octet & 0x02)

    if is_multicast:
        address_type = "Group"
        transmission = "Multicast"
    else:
        address_type = "Individual"
        transmission = "Unicast"

    if is_local:
        assignment = "Locally Administered"
    else:
        assignment = "Universally Administered"

    if is_local:
        vendor = "Not available — locally administered MAC"
    else:
        vendor = get_vendor(mac)

        if not vendor:
            vendor = "Vendor not found"

    data = {
        "mac": formatted_mac,
        "oui": oui,
        "vendor": vendor,
        "address_type": address_type,
        "assignment": assignment,
        "transmission": transmission,
        "oui_prefix": f"{oui[:2]}:{oui[2:4]}:{oui[4:6]}",
        "device_identifier": mac[6:],
    }

    result = []

    for key in FIELD_ORDER:
        value = data.get(key)

        if value is None or value == "":
            continue

        result.append({
            "label": FIELD_LABELS[key],
            "value": value,
        })

    return {
        "fields": result
    }