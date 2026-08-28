import requests
import phonenumbers

from urllib.parse import quote_plus
from phonenumbers import geocoder, carrier, timezone
from phonenumbers import PhoneNumberFormat, format_number


FIELD_LABELS = {
    "query": "Phone Number",
    "e164": "E.164",
    "international": "International Format",
    "national": "National Format",
    "country": "Country",
    "country_code": "Country Code",
    "calling_code": "Calling Code",
    "region": "Region",
    "location": "Location",
    "carrier": "Carrier",
    "line_type": "Line Type",
    "timezone": "UTC Offset",
    "possible": "Possible Number",
    "valid": "Valid Number",
}

FIELD_ORDER = [
    "query",
    "e164",
    "international",
    "national",
    "country",
    "country_code",
    "calling_code",
    "region",
    "location",
    "carrier",
    "line_type",
    "timezone",
    "possible",
    "valid",
]


TYPE_MAP = {
    0: "FIXED_LINE",
    1: "MOBILE",
    2: "FIXED_OR_MOBILE",
    3: "TOLL_FREE",
    4: "PREMIUM_RATE",
    5: "SHARED_COST",
    6: "VOIP",
    7: "PERSONAL_NUMBER",
    8: "PAGER",
    9: "UAN",
    10: "VOICEMAIL",
}


def normalize_phone(phone):
    phone = str(phone).strip()
    phone = phone.replace("＋", "+")
    phone = phone.replace("\u200e", "")
    phone = phone.replace("\u200f", "")
    phone = phone.replace("\u00a0", "")

    has_plus = phone.startswith("+")
    phone = "".join(c for c in phone if c.isdigit())

    if not phone:
        raise ValueError("Invalid phone number")

    if has_plus:
        phone = "+" + phone

    return phone


def parse_phone(phone):
    phone = normalize_phone(phone)

    try:
        parsed = phonenumbers.parse(phone, None)
    except phonenumbers.NumberParseException:
        raise ValueError("Invalid phone number")

    if not phonenumbers.is_possible_number(parsed):
        raise ValueError("Impossible phone number")

    return phone, parsed


def get_utc_offset(parsed):
    zones = timezone.time_zones_for_number(parsed)

    if not zones:
        return "Unknown"

    offset_map = {
        "Europe/Moscow": "UTC +03:00",
        "Asia/Baku": "UTC +04:00",
        "Asia/Yerevan": "UTC +04:00",
        "Asia/Tbilisi": "UTC +04:00",
        "Asia/Tashkent": "UTC +05:00",
        "Asia/Almaty": "UTC +05:00",
        "Asia/Shanghai": "UTC +08:00",
        "Asia/Tokyo": "UTC +09:00",
        "Europe/London": "UTC +00:00",
        "Europe/Paris": "UTC +01:00",
        "Europe/Berlin": "UTC +01:00",
        "America/New_York": "UTC -05:00",
        "America/Chicago": "UTC -06:00",
        "America/Denver": "UTC -07:00",
        "America/Los_Angeles": "UTC -08:00",
    }

    for zone in zones:
        if zone in offset_map:
            return offset_map[zone]

    return "Unknown"


def local_lookup(parsed):
    number_type = phonenumbers.number_type(parsed)

    region = geocoder.description_for_number(
        parsed,
        "en"
    ) or "Unknown"

    country = geocoder.country_name_for_number(
        parsed,
        "en"
    ) or "Unknown"

    return {
        "e164": format_number(
            parsed,
            PhoneNumberFormat.E164
        ),
        "international": format_number(
            parsed,
            PhoneNumberFormat.INTERNATIONAL
        ),
        "national": format_number(
            parsed,
            PhoneNumberFormat.NATIONAL
        ),
        "country": country,
        "country_code": (
            phonenumbers.region_code_for_number(parsed)
            or "Unknown"
        ),
        "calling_code": f"+{parsed.country_code}",
        "region": region,
        "location": region,
        "carrier": carrier.name_for_number(
            parsed,
            "en"
        ) or "Unknown",
        "line_type": TYPE_MAP.get(
            number_type,
            "UNKNOWN"
        ),
        "timezone": get_utc_offset(parsed),
        "possible": (
            "Yes"
            if phonenumbers.is_possible_number(parsed)
            else "No"
        ),
        "valid": (
            "Yes"
            if phonenumbers.is_valid_number(parsed)
            else "No"
        ),
    }


def public_api_lookup(phone):
    number = phone.lstrip("+")

    response = requests.get(
        f"https://libphonenumberapi.com/api/phone-numbers/{number}",
        timeout=8
    )

    response.raise_for_status()

    data = response.json()
    result = {}

    if data.get("is_valid") is not None:
        result["api_valid"] = (
            "Yes"
            if data["is_valid"]
            else "No"
        )

    formats = data.get("formats", {})

    if formats.get("e164"):
        result["e164"] = formats["e164"]

    if formats.get("international"):
        result["international"] = formats["international"]

    if formats.get("national"):
        result["national"] = formats["national"]

    if data.get("country"):
        result["country_code"] = data["country"]

    if data.get("carrier"):
        result["carrier"] = data["carrier"]

    if data.get("geo_name"):
        result["location"] = data["geo_name"]

    return result


def build_dorks(data):
    formats = [
        ("Google · E.164", "https://www.google.com/search?q=", data["e164"]),
        ("Google · International", "https://www.google.com/search?q=", data["international"]),
        ("Google · National", "https://www.google.com/search?q=", data["national"]),
        ("Bing · E.164", "https://www.bing.com/search?q=", data["e164"]),
        ("Bing · International", "https://www.bing.com/search?q=", data["international"]),
        ("Bing · National", "https://www.bing.com/search?q=", data["national"]),
        ("DuckDuckGo · E.164", "https://duckduckgo.com/?q=", data["e164"]),
        ("DuckDuckGo · International", "https://duckduckgo.com/?q=", data["international"]),
        ("DuckDuckGo · National", "https://duckduckgo.com/?q=", data["national"]),
    ]

    return [
        {
            "label": label,
            "url": url + quote_plus(f'"{number}"'),
            "query": number,
        }
        for label, url, number in formats
    ]

def phone_lookup(query):
    phone, parsed = parse_phone(query)

    data = {
        "query": phone
    }

    data.update(local_lookup(parsed))

    try:
        api_data = public_api_lookup(phone)
        data.update(api_data)
    except (requests.RequestException, ValueError):
        pass

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
        "fields": result,
        "dorks": build_dorks(data),
    }