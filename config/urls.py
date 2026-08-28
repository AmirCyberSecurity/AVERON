from django.shortcuts import redirect
from django.urls import path
from core import views


urlpatterns = [
    path("", views.menu, name="menu"),

    path("start", views.start, name="start"),
    path("start/", lambda request: redirect("start")),

    path("about", views.about, name="about"),
    path("about/", lambda request: redirect("about")),

    path("start/ip_lookup", views.ip_lookup, name="ip_lookup"),
    path("start/ip_lookup/", lambda request: redirect("ip_lookup")),
    path("start/ip_lookup/query/", views.ip_lookup_api, name="ip_lookup_api"),

    path("start/phone_lookup", views.phone_lookup, name="phone_lookup"),
    path("start/phone_lookup/", lambda request: redirect("phone_lookup")),
    path("start/phone_lookup/query/", views.phone_lookup_api, name="phone_lookup_api"),

    path("start/domain_lookup", views.domain_lookup, name="domain_lookup"),
    path("start/domain_lookup/", lambda request: redirect("domain_lookup")),
    path("start/domain_lookup/query/", views.domain_lookup_api, name="domain_lookup_api"),

    path("start/mac_lookup", views.mac_lookup, name="mac_lookup"),
    path("start/mac_lookup/", lambda request: redirect("mac_lookup")),
    path("start/mac_lookup/query/", views.mac_lookup_api, name="mac_lookup_api"),

    path("start/username_search", views.username_search, name="username_sarch"),
    path("start/username_search/", lambda request: redirect("username_search")),
    path("start/username_search/query/", views.username_search_api, name="username_search_api"),

    path("start/directory_lookup", views.directory_lookup, name="directory_lookup"),
    path("start/directory_lookup/", lambda request: redirect("directory_lookup")),
    path("start/directory_lookup/query/", views.directory_lookup_api, name="directory_lookup_api"),
]