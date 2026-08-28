from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.http import HttpResponse, JsonResponse

from core.lookups.ip_lookup import ip_lookup as perform_ip_lookup
from core.lookups.phone_lookup import phone_lookup as perform_phone_lookup
from core.lookups.domain_lookup import domain_lookup as perform_domain_lookup
from core.lookups.mac_lookup import mac_lookup as perform_mac_lookup
from core.lookups.username_search import username_search as perform_username_search
from core.lookups.directory_lookup import directory_lookup as perform_directory_lookup

from queue import Queue
import ipaddress
import threading
import asyncio
import json
import re

BAD_UA = [
    "python",
    "curl",
    "wget",
    "aiohttp",
    "requests",
    "httpx",
    "scrapy",
    "bot",
    "spider",
    "crawler",
    "mhddos",
    "dos",
    "ddos",
    "fsociety"
]


def is_bot(request):
    ua = request.headers.get("User-Agent", "").lower()

    if not ua:
        return True

    for bad in BAD_UA:
        if bad in ua:
            return True

    if "Accept-Language" not in request.headers:
        return True

    if "Accept" not in request.headers:
        return True

    return False


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")

    return ip


def menu(request):
    if is_bot(request):
        return HttpResponse(status=403)

    return render(request, "core/menu.html")


def start(request):
    if is_bot(request):
        return HttpResponse(status=403)

    return render(request, "core/start.html")


def about(request):
    if is_bot(request):
        return HttpResponse(status=403)

    return render(request, "core/about.html")


def ip_lookup(request):
    if is_bot(request):
        return HttpResponse(status=403)

    return render(request, "core/ip_lookup.html")


def ip_lookup_api(request):
    if is_bot(request):
        return JsonResponse(
            {"error": "Forbidden"},
            status=403
        )

    query = request.GET.get("query", "").strip()

    if not query:
        return JsonResponse(
            {"error": "IP address is required."},
            status=400
        )

    try:
        ipaddress.ip_address(query)
    except ValueError:
        return JsonResponse(
            {"error": "Invalid IP address."},
            status=400
        )

    try:
        data = perform_ip_lookup(query)

        if not data:
            return JsonResponse(
                {"error": "No data available for this IP address."},
                status=404
            )

        return JsonResponse(data)

    except Exception:
        return JsonResponse(
            {"error": "Internal server error."},
            status=500
        )

def phone_lookup(request):
    if is_bot(request):
        return HttpResponse(status=403)

    return render(request, "core/phone_lookup.html")


def phone_lookup_api(request):
    if is_bot(request):
        return JsonResponse(
            {"error": "Forbidden"},
            status=403
        )

    query = request.GET.get("query", "").strip()

    if not query:
        return JsonResponse(
            {"error": "Phone number is required."},
            status=400
        )

    if not query.startswith("+"):
        return JsonResponse(
            {"error": "Enter a phone number with country code, e.g. +994501234567."},
            status=400
        )

    if not query[1:].isdigit():
        return JsonResponse(
            {"error": "Phone number must contain only digits after +."},
            status=400
        )

    if not 7 <= len(query[1:]) <= 15:
        return JsonResponse(
            {"error": "Invalid phone number."},
            status=400
        )

    try:
        data = perform_phone_lookup(query)

        if not data:
            return JsonResponse(
                {"error": "No data available for this phone number."},
                status=404
            )

        return JsonResponse(data)

    except ValueError:
        return JsonResponse(
            {"error": "Invalid phone number."},
            status=400
        )

    except Exception:
        return JsonResponse(
            {"error": "Lookup failed."},
            status=400
        )
    
def domain_lookup(request):
    if is_bot(request):
        return HttpResponse(status=403)

    return render(request, "core/domain_lookup.html") 

def domain_lookup_api(request):
    if is_bot(request):
        return JsonResponse(
            {"error": "Forbidden"},
            status=403
        )

    query = request.GET.get("query", "").strip().lower()

    if not query:
        return JsonResponse(
            {"error": "Domain is required."},
            status=400
        )

    query = re.sub(r"^https?://", "", query)
    query = re.sub(r"^www\.", "", query)
    query = query.split("/")[0].split("?")[0].split("#")[0]

    if len(query) > 253:
        return JsonResponse(
            {"error": "Invalid domain."},
            status=400
        )

    if not re.fullmatch(
        r"(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}",
        query
    ):
        return JsonResponse(
            {"error": "Invalid domain."},
            status=400
        )

    try:
        data = perform_domain_lookup(query)

        if not data:
            return JsonResponse(
                {"error": "No data available for this domain."},
                status=404
            )

        return JsonResponse(data)

    except ValueError:
        return JsonResponse(
            {"error": "Invalid domain."},
            status=400
        )

    except Exception:
        return JsonResponse(
            {"error": "Internal server error."},
            status=500
        )

def mac_lookup(request):
    if is_bot(request):
        return HttpResponse(status=403)

    return render(request, "core/mac_lookup.html") 

def mac_lookup_api(request):
    if is_bot(request):
        return JsonResponse(
            {"error": "Forbidden"},
            status=403
        )

    query = request.GET.get("query", "").strip()

    if not query:
        return JsonResponse(
            {"error": "MAC address is required."},
            status=400
        )

    normalized = re.sub(r"[:-]", "", query)

    if len(normalized) != 12:
        return JsonResponse(
            {"error": "Invalid MAC address length."},
            status=400
        )

    if not re.fullmatch(r"[0-9a-fA-F]{12}", normalized):
        return JsonResponse(
            {"error": "Invalid MAC address."},
            status=400
        )

    try:
        data = perform_mac_lookup(query)

        if not data:
            return JsonResponse(
                {"error": "No data available for this MAC address."},
                status=404
            )

        return JsonResponse(data)

    except ValueError as e:
        return JsonResponse(
            {"error": str(e)},
            status=400
        )

    except Exception:
        return JsonResponse(
            {"error": "Internal server error."},
            status=500
        )

def username_search(request):
    if is_bot(request):
        return HttpResponse(status=403)

    return render(request, "core/username_search.html") 

def username_search_api(request):
    if is_bot(request):
        return JsonResponse(
            {"error": "Forbidden"},
            status=403
        )

    query = request.GET.get("query", "").strip()

    if not query:
        return JsonResponse(
            {"error": "Username is required."},
            status=400
        )

    if len(query) < 3 or len(query) > 20:
        return JsonResponse(
            {"error": "Username must be between 3 and 20 characters."},
            status=400
        )

    if not re.fullmatch(r"[A-Za-z0-9._-]{3,20}", query):
        return JsonResponse(
            {
                "error": "Username can contain only letters, numbers, dots, underscores and hyphens."
            },
            status=400
        )

    try:
        data = perform_username_search(query)

        if not data or not data.get("fields"):
            return JsonResponse(
                {"error": "No platforms found for this username."},
                status=404
            )

        return JsonResponse(data)

    except ValueError as e:
        return JsonResponse(
            {"error": str(e)},
            status=400
        )

    except Exception:
        return JsonResponse(
            {"error": "Username search failed."},
            status=500
        )


def directory_lookup(request):
    if is_bot(request):
        return HttpResponse(status=403)

    return render(request, "core/directory_lookup.html") 

def directory_lookup_api(request):
    if is_bot(request):
        return JsonResponse(
            {"error": "Forbidden"},
            status=403
        )

    query = request.GET.get("query", "").strip()

    if not query:
        return JsonResponse(
            {"error": "Domain is required."},
            status=400
        )

    if len(query) > 253:
        return JsonResponse(
            {"error": "Invalid domain."},
            status=400
        )

    def stream():
        queue = Queue()

        total = len(
            perform_directory_lookup.__globals__["DIRECTORIES"]
        )

        async def producer():
            try:
                async for item in perform_directory_lookup(query):
                    queue.put(("item", item))

            except ValueError as e:
                queue.put(("error", str(e)))

            except Exception:
                queue.put(("error", "Directory lookup failed."))

            finally:
                queue.put(("done", None))

        def run_producer():
            asyncio.run(producer())

        thread = threading.Thread(
            target=run_producer,
            daemon=True
        )

        thread.start()

        found = 0
        checked = 0

        data = {
            "message": "Starting directory lookup..."
        }

        yield "event: status\n"
        yield f"data: {json.dumps(data)}\n\n"

        while True:
            event_type, item = queue.get()

            if event_type == "item":

                if item["type"] == "result":
                    found += 1

                    data = {
                        "status": item["status"],
                        "path": item["path"],
                        "url": item["url"]
                    }

                    yield "event: result\n"
                    yield f"data: {json.dumps(data)}\n\n"

                elif item["type"] == "progress":
                    checked = item["checked"]

                    data = {
                        "checked": checked,
                        "total": item["total"]
                    }

                    yield "event: progress\n"
                    yield f"data: {json.dumps(data)}\n\n"

            elif event_type == "error":

                data = {
                    "message": item
                }

                yield "event: status\n"
                yield f"data: {json.dumps(data)}\n\n"

                break

            elif event_type == "done":

                data = {
                    "checked": checked,
                    "found": found
                }

                yield "event: complete\n"
                yield f"data: {json.dumps(data)}\n\n"

                break

    response = StreamingHttpResponse(
        stream(),
        content_type="text/event-stream"
    )

    response["Cache-Control"] = "no-cache, no-transform"
    response["X-Accel-Buffering"] = "no"

    return response