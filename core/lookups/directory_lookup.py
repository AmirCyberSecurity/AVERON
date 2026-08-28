import asyncio
import random
import string
import aiohttp

DIRECTORIES = [
    "/.htaccess", "/.htpasswd", "/.htaccess.bak", "/.htaccess.old", "/.htpasswd.bak", "/.env", "/.env.local", "/.env.production", "/.env.dev", "/.env.staging", "/.env.test", "/.env.example", "/.env.backup", "/.env.save",
    "/.env.1", "/.env.old", "/.git/config", "/.git/HEAD", "/.git/index", "/.git/logs/HEAD", "/.gitignore", "/.git/COMMIT_EDITMSG", "/.git/packed-refs", "/.git/info/exclude", "/.svn/entries", "/.svn/wc.db", "/.svn/text-base/", "/.bzr/",
    "/.hg/", "/.DS_Store", "/Thumbs.db", "/.dockerenv", "/docker-compose.yml", "/docker-compose.override.yml", "/.npmrc", "/.bowerrc", "/.editorconfig", "/.user.ini", "/web.config", "/web.config.bak", "/.well-known/", "/.well-known/security.txt",
    "/.well-known/apple-app-site-association", "/.well-known/assetlinks.json", "/.well-known/pki-validation/", "/.well-known/acme-challenge/", "/robots.txt", "/sitemap.xml", "/sitemap.xml.gz", "/sitemap.txt", "/crossdomain.xml", "/security.txt", "/humans.txt", "/LICENSE", "/LICENSE.txt", "/README.md",
    "/CHANGELOG.md", "/package.json", "/package-lock.json", "/yarn.lock", "/pnpm-lock.yaml", "/requirements.txt", "/Pipfile", "/Pipfile.lock", "/composer.json", "/composer.lock", "/Gemfile", "/Gemfile.lock", "/Makefile", "/Dockerfile",
    "/Dockerfile.dev", "/Dockerfile.prod", "/values.yaml", "/config", "/config.php", "/config.json", "/config.yml", "/config.yaml", "/config.inc.php", "/configuration.php", "/settings.py", "/settings.json", "/database.yml", "/db.json",
    "/credentials", "/credentials.json", "/secrets", "/secrets.json", "/keys", "/id_rsa", "/id_rsa.pub", "/vault", "/parameters.yml", "/appsettings.json", "/appsettings.Development.json", "/connections.json", "/config.bak", "/config.old",
    "/config.tmp", "/settings.php", "/admin", "/admin/", "/admin/login", "/admin/panel", "/admin/dashboard", "/admin/config", "/admin/users", "/admin/settings", "/admin/index.php", "/admin/index.html", "/admin_area", "/administrator",
    "/administrator/", "/adminpanel", "/controlpanel", "/cp", "/panel", "/dashboard", "/console", "/manager", "/manager/html", "/wp-admin", "/wp-admin/", "/wp-login.php", "/user/login", "/login",
    "/logon", "/auth/login", "/signin", "/cpanel", "/webmin", "/plesk", "/phpmyadmin", "/phpmyadmin/", "/pma", "/myadmin", "/dbadmin", "/pgadmin", "/mysql", "/sqlmanager",
    "/adminer.php", "/adminer", "/server-status", "/server-info", "/phpinfo.php", "/info.php", "/test.php", "/test.html", "/status", "/health", "/healthcheck", "/ping", "/heartbeat", "/healthz",
    "/readyz", "/livez", "/metrics", "/prometheus", "/grafana", "/kibana", "/elmah.axd", "/trace.axd", "/actuator", "/actuator/health", "/actuator/info", "/actuator/env", "/actuator/metrics", "/actuator/beans",
    "/actuator/loggers", "/actuator/heapdump", "/actuator/threaddump", "/actuator/mappings", "/actuator/configprops", "/actuator/httptrace", "/debug", "/debug/vars", "/debug/pprof", "/traceroute", "/trace", "/api", "/api/v1", "/api/v2",
    "/api/v3", "/v1", "/v2", "/v3", "/graphql", "/graphiql", "/graphql/console", "/graphql/explorer", "/playground", "/altair", "/voyager", "/swagger.json", "/swagger.yaml", "/swagger-ui.html",
    "/swagger-ui/", "/swagger-resources", "/openapi.json", "/openapi.yaml", "/api-docs", "/v2/api-docs", "/v3/api-docs", "/api/swagger.json", "/api/graphql", "/api/users", "/api/auth", "/api/admin", "/api/v1/users", "/api/v1/auth",
    "/api/v1/admin", "/api/v1/docs", "/api/v2/users", "/backup", "/backups", "/dump", "/dumps", "/database.sql", "/db.sql", "/backup.sql", "/backup.tar.gz", "/backup.zip", "/backup.tgz", "/site.zip",
    "/www.zip", "/app.zip", "/db.tar.gz", "/db.zip", "/dump.sql", "/dump.tar.gz", "/data.sql", "/users.sql", "/log", "/logs", "/error.log", "/access.log", "/debug.log", "/laravel.log",
    "/syslog", "/application.log", "/production.log", "/development.log", "/server.log", "/.bak", "/.old", "/.temp", "/.tmp", "/.swp", "/.swo", "/~", "/static", "/assets",
    "/uploads", "/files", "/images", "/img", "/css", "/js", "/media", "/public", "/storage", "/blob", "/cdn", "/temp", "/tmp", "/cache",
    "/webjars", "/vendor", "/node_modules", "/dist", "/build", "/register", "/signup", "/forgot-password", "/reset-password", "/logout", "/session", "/token", "/refresh", "/oauth",
    "/oauth2", "/saml", "/profile", "/settings", "/account", "/users", "/users/me", "/permissions", "/roles", "/groups", "/org", "/team", "/wp-content/", "/wp-includes/",
    "/wp-json/", "/xmlrpc.php", "/wp-config.php.bak", "/joomla", "/drupal", "/magento", "/gitlab", "/github", "/okta", "/auth0", "/firebase", "/404", "/500", "/503",
    "/maintenance", "/setup", "/install", "/installation", "/configure", "/migrate", "/upgrade", "/update", "/patch", "/hotfix", "/index.html", "/index.php", "/index.asp", "/index.jsp",
    "/default.aspx", "/main.js", "/app.js", "/home", "/about", "/contact", "/help", "/support", "/terms", "/privacy", "/cookie", "/cookies", "/policy", "/license",
    "/version", "/versions", "/beta", "/alpha", "/staging", "/dev", "/development", "/production", "/preview", "/cdn-cgi/", "/database", "/db", "/sql", "/pgsql", "/mongo",
    "/redis", "/elasticsearch", "/solr", "/swagger-resources", "/v2/api-docs", "/v3/api-docs", "/api/swagger.json", "/openapi.yaml", "/api/graphql", "/graphql/console", "/graphql/explorer", "/playground", "/voyager", "/altair",
    "/wordpress", "/wp-content/", "/wp-includes/", "/wp-json/", "/wp-login.php", "/xmlrpc.php", "/joomla", "/drupal", "/magento", "/gitlab", "/github", "/okta", "/auth0", "/firebase",
    "/storage", "/blob", "/cdn", "/media", "/public", "/temp", "/tmp", "/cache", "/log", "/logs", "/error", "/errors", "/404", "/500",
    "/503", "/maintenance", "/setup", "/install", "/installation", "/configure", "/migrate", "/upgrade", "/update", "/patch", "/hotfix", "/api/v1/users", "/api/v1/admin", "/api/v1/auth",
    "/api/v1/orders", "/api/v1/products", "/api/v1/reports", "/api/v1/analytics", "/api/v1/export", "/api/v1/import", "/api/v1/upload", "/api/v1/download", "/api/v1/search", "/api/v1/notifications", "/api/v1/messages", "/api/v1/comments", "/api/v1/reviews", "/api/v2/users",
    "/api/v2/admin", "/api/v2/auth", "/api/v2/orders", "/api/v2/products", "/api/v2/reports", "/api/v2/analytics", "/api/v2/export", "/api/v2/import", "/api/v2/search", "/confidential", "/sensitive", "/private", "/restricted", "/internal",
    "/secret", "/hidden", "/credentials.xml", "/secrets.yml", "/config.xml", "/settings.xml", "/db.xml", "/data.json", "/backup.json", "/dump.json", "/users.json", "/export.json", "/import.json", "/logs.txt",
    "/error.txt", "/debug.txt", "/access.txt", "/server.txt", "/info.txt", "/status.txt", "/out.log", "/err.log", "/stdout.log", "/stderr.log", "/audit.log", "/security.log", "/auth.log", "/system.log",
    "/cron.log", "/nginx.log", "/apache.log", "/httpd.log", "/php.log", "/mysql.log", "/postgres.log", "/redis.log", "/mongo.log", "/elastic.log", "/docker.log", "/kube.log", "/deploy.log", "/build.log",
    "/test.log", "/ci.log", "/cd.log", "/pipeline.log", "/job.log", "/task.log", "/worker.log", "/queue.log", "/event.log", "/trace.log", "/metric.log", "/stat.log", "/report.log", "/summary.log",
    "/detail.log", "/history.log", "/archive.log", "/old.log", "/bak.log", "/temp.log", "/tmp.log", "/cache.log", "/store.log", "/data.log", "/db.log", "/sql.log", "/query.log", "/slow.log",
    "/error_log", "/access_log", "/debug_log", "/ssl_error_log", "/ssl_access_log", "/ssl_request_log", "/rewrite.log", "/proxy.log", "/balancer.log", "/cgi.log", "/fcgi.log", "/php-fpm.log", "/wsgi.log", "/asgi.log",
    "/unicorn.log", "/puma.log", "/passenger.log", "/gunicorn.log", "/uvicorn.log", "/hypercorn.log", "/waitress.log", "/cherrypy.log", "/tornado.log", "/twisted.log", "/sanic.log", "/fastapi.log", "/flask.log", "/django.log",
    "/rails.log", "/express.log", "/koa.log", "/nest.log", "/next.log", "/nuxt.log", "/gatsby.log", "/astro.log", "/remix.log", "/svelte.log", "/vue.log", "/react.log", "/angular.log", "/ember.log",
    "/backbone.log", "/knockout.log", "/jquery.log", "/bootstrap.log", "/tailwind.log", "/sass.log", "/less.log", "/stylus.log", "/webpack.log", "/vite.log", "/rollup.log", "/esbuild.log", "/parcel.log", "/gulp.log",
    "/grunt.log", "/bower.log", "/npm.log", "/yarn.log", "/pnpm.log", "/bun.log", "/deno.log", "/composer.log", "/pip.log", "/poetry.log", "/pipenv.log", "/conda.log", "/gem.log", "/bundler.log",
    "/cargo.log", "/go.log", "/maven.log", "/gradle.log", "/sbt.log", "/ant.log", "/bazel.log", "/ninja.log", "/cmake.log", "/make.log", "/vcpkg.log", "/conan.log", "/nuget.log", "/dotnet.log",
    "/mono.log", "/cocoapods.log", "/carthage.log", "/swift.log", "/apk.log", "/ipa.log", "/exe.log", "/msi.log", "/dmg.log", "/pkg.log", "/deb.log", "/rpm.log", "/flatpak.log", "/snap.log",
    "/appimage.log", "/docker.tar", "/container.tar", "/image.tar", "/export.tar", "/import.tar", "/db.tar", "/data.tar", "/site.tar", "/www.tar", "/app.tar", "/core.tar", "/sys.tar", "/root.tar",
    "/user.tar", "/home.tar", "/var.tar", "/etc.tar", "/opt.tar", "/usr.tar", "/srv.tar", "/mnt.tar", "/media.tar", "/tmp.tar", "/temp.tar", "/cache.tar", "/store.tar", "/vault.tar",
    "/backup.tgz", "/site.tgz", "/www.tgz", "/app.tgz", "/db.tgz", "/data.tgz", "/export.tgz", "/import.tgz", "/logs.tgz", "/core.tgz", "/sys.tgz", "/root.tgz", "/user.tgz", "/home.tgz",
    "/backup.rar", "/site.rar", "/www.rar", "/app.rar", "/db.rar", "/data.rar", "/export.rar", "/import.rar", "/logs.rar", "/core.rar", "/sys.rar", "/root.rar", "/user.rar", "/home.rar",
    "/backup.7z", "/site.7z", "/www.7z", "/app.7z", "/db.7z", "/data.7z", "/export.7z", "/import.7z", "/logs.7z", "/core.7z", "/sys.7z", "/root.7z", "/user.7z", "/home.7z"
]


def clean_domain(query):
    query = query.strip().lower()
    query = query.removeprefix("https://")
    query = query.removeprefix("http://")
    query = query.removeprefix("www.")
    return query.split("/")[0].split("?")[0].split("#")[0]


def random_path():
    return "/__averon_" + "".join(
        random.choices(
            string.ascii_lowercase + string.digits,
            k=24
        )
    )


async def directory_lookup(query, concurrency=10):
    domain = clean_domain(query)
    base = f"https://{domain}"

    timeout = aiohttp.ClientTimeout(
        total=8,
        connect=4,
        sock_read=6
    )

    connector = aiohttp.TCPConnector(
        limit=concurrency,
        limit_per_host=concurrency,
        ssl=False
    )

    async with aiohttp.ClientSession(
        timeout=timeout,
        connector=connector,
        headers={
            "User-Agent": "AVERON/1.0",
            "Accept": "*/*"
        }
    ) as session:

        try:
            async with session.get(
                base + random_path(),
                allow_redirects=False
            ) as response:
                baseline_status = response.status
                baseline_body = await response.read()
                baseline_size = len(baseline_body)
                baseline_type = response.content_type

        except Exception:
            raise ValueError("Website could not be reached")

        semaphore = asyncio.Semaphore(concurrency)

        async def check(path):
            async with semaphore:
                try:
                    async with session.get(
                        base + path,
                        allow_redirects=False
                    ) as response:

                        status = response.status

                        if status in (404, 307, 308, 301):
                            return None

                        body = await response.read()

                        if status == baseline_status:
                            size = len(body)

                            if (
                                abs(size - baseline_size)
                                / max(size, baseline_size, 1)
                                < 0.05
                                and response.content_type == baseline_type
                            ):
                                return None

                        return {
                            "status": status,
                            "path": path,
                            "url": base + path
                        }

                except (
                    asyncio.TimeoutError,
                    aiohttp.ClientError
                ):
                    return None

        tasks = [
            asyncio.create_task(check(path))
            for path in DIRECTORIES
        ]

        total = len(tasks)
        checked = 0

        for task in asyncio.as_completed(tasks):
            result = await task
            checked += 1

            if result:
                yield {
                    "type": "result",
                    "status": result["status"],
                    "path": result["path"],
                    "url": result["url"]
                }

            yield {
                "type": "progress",
                "checked": checked,
                "total": total
            }