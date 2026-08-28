import re
import requests

from concurrent.futures import ThreadPoolExecutor, as_completed


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/142.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


PLATFORMS = [

    {
        "name": "GitHub",
        "url": "https://github.com/{username}",
        "not_found": [
            "Not Found",
            "This is not the web page you are looking for"
        ],
    },

    {
        "name": "GitLab",
        "url": "https://gitlab.com/{username}",
        "not_found": [
            "404",
            "Page Not Found",
        ],
    },

    {
        "name": "Codeberg",
        "url": "https://codeberg.org/{username}",
        "not_found": [
            "Page Not Found",
            "The page you are looking for could not be found",
        ],
    },

    {
        "name": "Bitbucket",
        "url": "https://bitbucket.org/{username}/",
        "not_found": [
            "Page not found",
        ],
    },

    {
        "name": "SourceForge",
        "url": "https://sourceforge.net/u/{username}/",
        "not_found": [
            "Page not found",
        ],
    },

    {
        "name": "Gitee",
        "url": "https://gitee.com/{username}",
        "not_found": [
            "Page not found",
        ],
    },

    {
        "name": "HackerOne",
        "url": "https://hackerone.com/{username}",
        "not_found": [
            "Page not found",
        ],
    },

    {
        "name": "Bugcrowd",
        "url": "https://bugcrowd.com/{username}",
        "not_found": [
            "Page not found",
        ],
    },

    {
        "name": "Twitch",
        "url": "https://www.twitch.tv/{username}",
        "not_found": [
            "Sorry. Unless you've got a time machine",
            "This channel is unavailable",
        ],
    },

    {
        "name": "X",
        "url": "https://x.com/{username}",
        "not_found": [
            "This account doesn't exist",
            "This account doesn’t exist",
        ],
    },

    {
        "name": "Facebook",
        "url": "https://www.facebook.com/{username}",
        "not_found": [
            "This page isn't available",
            "This content isn't available",
        ],
    },

    {
        "name": "Pinterest",
        "url": "https://www.pinterest.com/{username}/",
        "not_found": [
            "Page not found",
        ],
    },

    {
        "name": "LinkedIn",
        "url": "https://www.linkedin.com/in/{username}/",
        "not_found": [
            "Page not found",
            "This page doesn't exist",
        ],
    },

    {
        "name": "Telegram",
        "url": "https://t.me/{username}",
        "not_found": [
            "If you have Telegram",
        ],
    },

    {
        "name": "Discord",
        "url": "https://discord.com/users/{username}",
        "not_found": [
            "Unknown User",
        ],
    },

    {
        "name": "Steam",
        "url": "https://steamcommunity.com/id/{username}",
        "not_found": [
            "The specified profile could not be found",
        ],
    },

    {
        "name": "Medium",
        "url": "https://medium.com/@{username}",
        "not_found": [
            "Page not found",
        ],
    },

    {
        "name": "Dev.to",
        "url": "https://dev.to/{username}",
        "not_found": [
            "404",
        ],
    },

    {
        "name": "CodePen",
        "url": "https://codepen.io/{username}",
        "not_found": [
            "404",
        ],
    },

    {
        "name": "Replit",
        "url": "https://replit.com/@{username}",
        "not_found": [
            "404",
        ],
    },

    {
        "name": "Hugging Face",
        "url": "https://huggingface.co/{username}",
        "not_found": [
            "404",
        ],
    },

    {
        "name": "Kaggle",
        "url": "https://www.kaggle.com/{username}",
        "not_found": [
            "404",
        ],
    },

    {
        "name": "Docker Hub",
        "url": "https://hub.docker.com/u/{username}",
        "not_found": [
            "404",
        ],
    },

    {
        "name": "Keybase",
        "url": "https://keybase.io/{username}",
        "not_found": [
            "404",
        ],
    },

    {
        "name": "SoundCloud",
        "url": "https://soundcloud.com/{username}",
        "not_found": [
            "We can't find that page",
            "Page not found",
        ],
    },

    {
        "name": "Bandcamp",
        "url": "https://bandcamp.com/{username}",
        "not_found": [
            "Sorry, that page doesn't exist",
        ],
    },

    {
        "name": "Last.fm",
        "url": "https://www.last.fm/user/{username}",
        "not_found": [
            "Page not found",
        ],
    },

    {
        "name": "Letterboxd",
        "url": "https://letterboxd.com/{username}/",
        "not_found": [
            "Page not found",
        ],
    },

    {
        "name": "Goodreads",
        "url": "https://www.goodreads.com/user/show/{username}",
        "not_found": [
            "Page not found",
        ],
    },

    {
        "name": "Vimeo",
        "url": "https://vimeo.com/{username}",
        "not_found": [
            "Page not found",
        ],
    },

    {
        "name": "Flickr",
        "url": "https://www.flickr.com/people/{username}/",
        "not_found": [
            "Page not found",
        ],
    },

    {
        "name": "Behance",
        "url": "https://www.behance.net/{username}",
        "not_found": [
            "Page Not Found",
        ],
    },

    {
        "name": "Dribbble",
        "url": "https://dribbble.com/{username}",
        "not_found": [
            "Page not found",
        ],
    },

    {
        "name": "Unsplash",
        "url": "https://unsplash.com/@{username}",
        "not_found": [
            "Page not found",
        ],
    },

    {
        "name": "Gravatar",
        "url": "https://gravatar.com/{username}",
        "not_found": [
            "Page not found",
        ],
    },

    {
        "name": "About.me",
        "url": "https://about.me/{username}",
        "not_found": [
            "Page not found",
        ],
    },

    {
        "name": "Patreon",
        "url": "https://www.patreon.com/{username}",
        "not_found": [
            "Page not found",
        ],
    },

    {
        "name": "Buy Me a Coffee",
        "url": "https://buymeacoffee.com/{username}",
        "not_found": [
            "Page not found",
        ],
    },

    {
        "name": "Product Hunt",
        "url": "https://www.producthunt.com/@{username}",
        "not_found": [
            "Page not found",
        ],
    },

    {
        "name": "npm",
        "url": "https://www.npmjs.com/~{username}",
        "not_found": [
            "404",
        ],
    },

    {
        "name": "Stack Overflow",
        "url": "https://stackoverflow.com/users/{username}",
        "not_found": [
            "Page not found",
        ],
    },

    {
        "name": "Stack Exchange",
        "url": "https://stackexchange.com/users/{username}",
        "not_found": [
            "Page not found",
        ],
    },

    {
        "name": "Mixcloud",
        "url": "https://www.mixcloud.com/{username}/",
        "not_found": [
            "Page not found",
        ],
    },

    {
        "name": "Disqus",
        "url": "https://disqus.com/by/{username}/",
        "not_found": [
            "Page not found",
        ],
    },

    {
        "name": "VK",
        "url": "https://vk.com/{username}",
        "not_found": [
            "Page not found",
            "This page is unavailable",
        ],
    },
]


def normalize_username(username):
    username = username.strip()

    if not re.fullmatch(r"[A-Za-z0-9._-]{3,20}", username):
        raise ValueError(
            "Username must contain only letters, numbers, dots, underscores "
            "or hyphens and be between 3 and 20 characters."
        )

    return username


def check_platform(platform, username):
    url = platform["url"].format(username=username)

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=7,
            allow_redirects=True
        )

        if response.status_code >= 400:
            return None

        final_url = response.url
        body = response.text[:500000]

        for marker in platform.get("not_found", []):
            if marker.lower() in body.lower():
                return None

        if username.lower() not in final_url.lower():
            return None

        return {
            "label": platform["name"],
            "value": username,
            "url": final_url,
            "status": response.status_code,
        }

    except requests.RequestException:
        return None


def username_search(username):
    username = normalize_username(username)

    results = []

    with ThreadPoolExecutor(
        max_workers=min(20, len(PLATFORMS))
    ) as executor:

        futures = {
            executor.submit(
                check_platform,
                platform,
                username
            ): platform
            for platform in PLATFORMS
        }

        for future in as_completed(futures):
            try:
                result = future.result()

                if result:
                    results.append(result)

            except Exception:
                continue

    results.sort(
        key=lambda item: item["label"].lower()
    )

    return {
        "fields": results
    }