import asyncio
import random
import string
import aiohttp

DIRECTORIES = [
    "/.env", "/.env.local", "/.env.production", "/.env.dev", "/.env.staging", "/.env.test", "/.env.example", "/.env.backup", "/.env.save",
    "/.env.1", "/.env.old", "/.env.bak", "/.env.tmp", "/.env.temp", "/.env.json", "/.env.yaml", "/.env.php", "/.env.db",
    "/.env.dist", "/.env.sample", "/.env.ci", "/.env.docker", "/.env.k8s", "/.env.kube", "/.env.aws", "/.env.gcp", "/.env.azure",
    "/.env.prod", "/.env.stage", "/.env.testing", "/.env.development", "/.env.default", "/.env.override", "/.env.secret",
    "/.env.credentials", "/.env.db.local", "/.env.app", "/.env.web", "/.env.api", "/.env.server", "/.env.client",
    "/app/.env", "/app/.env.local", "/app/.env.production", "/backend/.env", "/frontend/.env", "/api/.env", "/server/.env", "/client/.env",
    "/service/.env", "/services/.env", "/microservice/.env", "/docker/.env", "/deploy/.env", "/deployment/.env", "/env/.env", "/envs/.env",
    "/config/.env", "/configs/.env", "/secrets/.env", "/private/.env", "/internal/.env", "/secure/.env", "/data/.env", "/database/.env",
    "/db/.env", "/storage/.env", "/public/.env", "/src/.env", "/dist/.env", "/build/.env", "/test/.env", "/tests/.env", "/staging/.env",
    "/production/.env", "/dev/.env", "/development/.env", "/local/.env", "/example/.env", "/sample/.env", "/template/.env", "/default/.env",
    "/base/.env", "/main/.env", "/core/.env", "/common/.env", "/shared/.env", "/global/.env", "/local.env", "/production.env", "/development.env",
    "/staging.env", "/test.env", "/example.env", "/sample.env", "/template.env", "/default.env", "/config.env", "/settings.env", "/secret.env",
    "/credentials.env", "/passwords.env", "/tokens.env", "/keys.env", "/certificates.env", "/certs.env", "/ssl.env", "/ssh.env", "/git.env",
    "/aws.env", "/azure.env", "/gcp.env", "/cloud.env", "/db.env", "/database.env", "/mysql.env", "/postgres.env", "/redis.env", "/mongo.env",
    "/elasticsearch.env", "/rabbitmq.env", "/kafka.env", "/docker.env", "/compose.env", "/kubernetes.env", "/k8s.env", "/helm.env", "/terraform.env",
    "/var/www/html/.env", "/var/www/.env", "/site/.env", "/web/.env", "/www/.env", "/project/.env", "/core/.env.local",

    "/.git/config", "/.git/HEAD", "/.git/index", "/.git/logs/HEAD", "/.gitignore", "/.git/COMMIT_EDITMSG", "/.git/packed-refs", "/.git/info/exclude",
    "/.git/refs/heads/main", "/.git/refs/heads/master", "/.git/refs/heads/develop", "/.git/refs/heads/staging", "/.git/refs/tags/",
    "/.git/config.worktree", "/.gitmodules", "/.gitattributes", "/.git/FETCH_HEAD", "/.git/ORIG_HEAD", "/.git/description",
    "/.git/hooks/pre-commit.sample", "/.git/hooks/post-commit", "/.git/hooks/pre-push.sample", "/.git/info/refs", "/.git/objects/info/packs",
    "/.svn/entries", "/.svn/wc.db", "/.svn/text-base/", "/.svn/all-wcprops", "/.svn/prop-base/", "/.svn/pristine/",
    "/.bzr/", "/.bzr/branch-format", "/.hg/", "/.hg/hgrc", "/.hg/requires", "/.hg/dirstate",

    "/.htaccess", "/.htpasswd", "/.htaccess.bak", "/.htaccess.old", "/.htaccess.save", "/.htaccess.tmp", "/.htpasswd.bak", "/.htpasswd.old",
    "/.user.ini", "/web.config", "/web.config.bak", "/web.config.old", "/web.Debug.config", "/web.Release.config", "/web.config.txt",
    "/.DS_Store", "/Thumbs.db", "/.dockerenv", "/docker-compose.yml", "/docker-compose.override.yml", "/docker-compose.dev.yml", "/docker-compose.prod.yml",
    "/docker-compose.staging.yml", "/docker-compose.test.yml", "/docker-compose.local.yml", "/Dockerfile", "/Dockerfile.dev", "/Dockerfile.prod",
    "/Dockerfile.staging", "/Dockerfile.test", "/Dockerfile.local", "/Dockerfile.build", "/.docker/config.json",
    "/.npmrc", "/.bowerrc", "/.editorconfig", "/.eslintrc", "/.eslintrc.js", "/.eslintrc.json", "/.prettierrc", "/.babelrc",
    "/Procfile", "/Procfile.options", "/fly.toml", "/render.yaml", "/vercel.json", "/netlify.toml", "/app.json", "/serverless.yml",

    "/.well-known/", "/.well-known/security.txt", "/.well-known/apple-app-site-association", "/.well-known/assetlinks.json",
    "/.well-known/pki-validation/", "/.well-known/acme-challenge/", "/.well-known/openid-configuration", "/.well-known/jwks.json",
    "/.well-known/matrix/client", "/.well-known/matrix/server", "/.well-known/webfinger", "/.well-known/change-password",
    "/robots.txt", "/sitemap.xml", "/sitemap.xml.gz", "/sitemap.txt", "/sitemap_index.xml", "/crossdomain.xml", "/security.txt",
    "/humans.txt", "/LICENSE", "/LICENSE.txt", "/README.md", "/CHANGELOG.md", "/CONTRIBUTING.md", "/SECURITY.md",

    "/package.json", "/package-lock.json", "/yarn.lock", "/pnpm-lock.yaml", "/bun.lockb", "/requirements.txt", "/Pipfile", "/Pipfile.lock",
    "/poetry.lock", "/pyproject.toml", "/composer.json", "/composer.lock", "/Gemfile", "/Gemfile.lock", "/Makefile", "/values.yaml",
    "/Chart.yaml", "/build.gradle", "/build.gradle.kts", "/pom.xml", "/Cargo.toml", "/Cargo.lock", "/go.mod", "/go.sum", "/mix.exs", "/mix.lock",
    "/packages.config", "/Project.csproj", "/App.config", "/deps.edn", "/project.clj", "/pubspec.yaml", "/pubspec.lock",

    "/config", "/config.php", "/config.json", "/config.yml", "/config.yaml", "/config.inc.php", "/configuration.php", "/settings.py", "/settings.json",
    "/database.yml", "/db.json", "/credentials", "/credentials.json", "/secrets", "/secrets.json", "/keys", "/id_rsa", "/id_rsa.pub", "/vault",
    "/parameters.yml", "/appsettings.json", "/appsettings.Development.json", "/appsettings.Production.json", "/appsettings.Staging.json",
    "/connections.json", "/config.bak", "/config.old", "/config.tmp", "/settings.php", "/credentials.xml", "/secrets.yml", "/config.xml",
    "/settings.xml", "/db.xml", "/data.json", "/auth.json", "/tokens.json", "/keys.json", "/jwt.json", "/api_key.txt", "/apikeys.json",

    "/admin", "/admin/", "/admin/login", "/admin/panel", "/admin/dashboard", "/admin/config", "/admin/users", "/admin/settings", "/admin/index.php",
    "/admin/index.html", "/admin_area", "/administrator", "/administrator/", "/adminpanel", "/controlpanel", "/cp", "/panel", "/dashboard",
    "/console", "/manager", "/manager/html", "/manager/status", "/wp-admin", "/wp-admin/", "/wp-login.php", "/user/login", "/login", "/logon",
    "/auth/login", "/signin", "/cpanel", "/webmin", "/plesk", "/phpmyadmin", "/phpmyadmin/", "/pma", "/myadmin", "/dbadmin", "/pgadmin",
    "/mysql", "/sqlmanager", "/adminer.php", "/adminer", "/chive", "/phppgadmin", "/pma/", "/db/", "/sql/", "/mysqladmin/",

    "/server-status", "/server-info", "/phpinfo.php", "/info.php", "/test.php", "/test.html", "/status", "/health", "/healthcheck", "/ping",
    "/heartbeat", "/healthz", "/readyz", "/livez", "/metrics", "/prometheus", "/grafana", "/kibana", "/elmah.axd", "/trace.axd",
    "/actuator", "/actuator/health", "/actuator/info", "/actuator/env", "/actuator/metrics", "/actuator/beans", "/actuator/loggers",
    "/actuator/heapdump", "/actuator/threaddump", "/actuator/mappings", "/actuator/configprops", "/actuator/httptrace", "/actuator/logfile",
    "/actuator/flyway", "/actuator/liquibase", "/actuator/auditevents", "/actuator/caches", "/actuator/conditions", "/actuator/scheduledtasks",
    "/debug", "/debug/vars", "/debug/pprof", "/debug/default/view", "/_profiler/", "/_profiler/phpinfo", "/traceroute", "/trace",

    "/api", "/api/v1", "/api/v2", "/api/v3", "/v1", "/v2", "/v3", "/graphql", "/graphiql", "/graphql/console", "/graphql/explorer",
    "/playground", "/altair", "/voyager", "/swagger.json", "/swagger.yaml", "/swagger-ui.html", "/swagger-ui/", "/swagger-resources",
    "/openapi.json", "/openapi.yaml", "/api-docs", "/v2/api-docs", "/v3/api-docs", "/api/swagger.json", "/api/graphql", "/api/users",
    "/api/auth", "/api/admin", "/api/v1/users", "/api/v1/auth", "/api/v1/admin", "/api/v1/docs", "/api/v2/users", "/redoc",
    "/schema.graphql", "/api/v1/health", "/api/v1/status", "/api/v1/ping", "/grpc.reflection.v1alpha.ServerReflection",

    "/backup", "/backups", "/dump", "/dumps", "/database.sql", "/db.sql", "/backup.sql", "/backup.tar.gz", "/backup.zip", "/backup.tgz",
    "/site.zip", "/www.zip", "/app.zip", "/db.tar.gz", "/db.zip", "/dump.sql", "/dump.tar.gz", "/data.sql", "/users.sql", "/backup.rar",
    "/site.rar", "/www.rar", "/app.rar", "/db.rar", "/data.rar", "/export.rar", "/import.rar", "/logs.rar", "/core.rar", "/sys.rar",
    "/root.rar", "/user.rar", "/home.rar", "/backup.7z", "/site.7z", "/www.7z", "/app.7z", "/db.7z", "/data.7z", "/export.7z", "/import.7z",
    "/logs.7z", "/core.7z", "/sys.7z", "/root.7z", "/user.7z", "/home.7z", "/dump.sql.gz", "/backup.sql.gz", "/dump.rdb", "/database.sql.zip",
    "/database.sql.tar.gz", "/db.sql.gz", "/db.sql.bz2", "/backup.sql.bz2", "/backup.tar.bz2", "/backup.zip.bak", "/dump.sql.bak",
    "/dump.sql.old", "/dump.sql.txt", "/backup.sql.txt", "/export.sql", "/export.sql.gz", "/export.sql.zip", "/import.sql", "/sql.tar.gz",
    "/sql.zip", "/mysql.sql", "/mysql.sql.gz", "/postgres.sql", "/postgres.sql.gz", "/pgsql.sql", "/sqlite.db", "/sqlite3.db",
    "/sqlite.sqlite", "/sqlite3.sqlite3", "/data.sqlite", "/data.sqlite3", "/test.sqlite", "/test.sqlite3", "/dev.sqlite", "/dev.sqlite3",
    "/prod.sqlite", "/prod.sqlite3", "/staging.sqlite", "/database.db", "/database.db3", "/db.sqlite", "/db.sqlite3", "/database.sqlite",
    "/database.sqlite3", "/db.bak", "/db.old", "/db.save", "/db.temp", "/db.tmp", "/database.bak", "/database.old", "/database.save",
    "/database.temp", "/database.tmp", "/backup.tar", "/db.tar", "/dump.tar", "/site.tar", "/www.tar", "/app.tar", "/data.tar",

    "/log", "/logs", "/error.log", "/access.log", "/debug.log", "/laravel.log", "/syslog", "/application.log", "/production.log",
    "/development.log", "/server.log", "/logs.txt", "/error.txt", "/debug.txt", "/access.txt", "/server.txt", "/info.txt", "/status.txt",
    "/out.log", "/err.log", "/stdout.log", "/stderr.log", "/audit.log", "/security.log", "/auth.log", "/system.log", "/cron.log",
    "/nginx.log", "/apache.log", "/httpd.log", "/php.log", "/mysql.log", "/postgres.log", "/redis.log", "/mongo.log", "/elastic.log",
    "/docker.log", "/kube.log", "/deploy.log", "/build.log", "/test.log", "/ci.log", "/cd.log", "/pipeline.log", "/slow.log",
    "/error_log", "/access_log", "/debug_log", "/ssl_error_log", "/ssl_access_log", "/ssl_request_log", "/rewrite.log", "/proxy.log",
    "/storage/logs/laravel.log", "/var/log/auth.log", "/var/log/syslog", "/var/log/nginx/access.log", "/var/log/nginx/error.log",
    "/var/log/apache2/access.log", "/var/log/apache2/error.log", "/logs/error.log", "/logs/access.log", "/logs/debug.log",

    "/wp-content/", "/wp-includes/", "/wp-json/", "/xmlrpc.php", "/wp-config.php", "/wp-config.php.bak", "/wp-config.php.txt",
    "/wp-config.php.old", "/wp-config.php.save", "/wp-config.old", "/wp-config.bak", "/joomla", "/drupal", "/magento", "/gitlab", "/github",
    "/okta", "/auth0", "/firebase", "/manage.py", "/WEB-INF/web.xml", "/WEB-INF/applicationContext.xml", "/META-INF/MANIFEST.MF",
    "/.aws/credentials", "/.aws/config", "/.kube/config", "/Kubeconfig", "/.github/workflows/", "/.gitlab-ci.yml", "/Jenkinsfile",
    "/terraform.tfstate", "/terraform.tfstate.backup", "/.terraform/", "/.terraform.lock.hcl", "/server.key", "/server.crt", "/privkey.pem",
    "/fullchain.pem", "/cert.pem", "/chain.pem", "/.ssh/id_rsa", "/.ssh/id_rsa.pub", "/.ssh/id_ed25519", "/.ssh/authorized_keys",
    "/.ssh/known_hosts", "/.vscode/settings.json", "/.idea/workspace.xml", "/.idea/webServers.xml", "/.idea/vcs.xml",

    "/config/database.yml", "/config/secrets.yml", "/config/application.yml", "/config/parameters.yml", "/config/config.json",
    "/config/settings.json", "/settings/settings.json", "/app/config/parameters.yml", "/protected/config/main.php",
    "/protected/config/params.php", "/protected/config/db.php", "/bitrix/php_interface/dbconn.php", "/bitrix/.settings.php",
    "/local/php_interface/dbconn.php", "/system/config/database.php", "/application/config/database.php", "/application/config/config.php",
    "/core/config/config.php", "/include/config.php", "/inc/config.php", "/config/database.php", "/config/db.php", "/config/configuration.php",
    "/inc/db.php", "/include/db.php", "/common/config/main-local.php", "/frontend/config/main-local.php", "/backend/config/main-local.php",
    "/config/jwt.json", "/config/aws.json", "/config/redis.php", "/config/cache.php", "/config/session.php",

    "/etc/environment", "/etc/passwd", "/etc/shadow", "/etc/hosts", "/etc/resolv.conf", "/etc/nginx/nginx.conf", "/etc/apache2/apache2.conf",
    "/etc/php/php.ini", "/etc/mysql/my.cnf", "/etc/redis/redis.conf", "/proc/self/environ", "/proc/self/cmdline", "/proc/self/fd/",
    "/proc/version", "/proc/cpuinfo", "/proc/meminfo", "/proc/net/tcp", "/proc/net/arp", "/proc/net/route", "/sys/class/net/",
    "/root/.bash_history", "/root/.ssh/authorized_keys", "/home/user/.bash_history", "/home/user/.ssh/id_rsa", "/var/mail/root",
    "/var/spool/mail/root", "/etc/crontab", "/etc/cron.d/", "/etc/issue", "/etc/motd", "/etc/group", "/etc/sudoers",

    "/_next/data/", "/_next/static/", "/_nuxt/", "/.next/cache/", "/.next/server/", "/.nuxt/", "/build/manifest.json", "/dist/manifest.json",
    "/mix-manifest.json", "/asset-manifest.json", "/.svelte-kit/", "/.astro/", "/.output/server/", "/.output/public/",

    "/static", "/assets", "/uploads", "/files", "/images", "/img", "/css", "/js", "/media", "/public", "/storage", "/blob", "/cdn",
    "/temp", "/tmp", "/cache", "/webjars", "/vendor", "/node_modules", "/dist", "/build", "/confidential", "/sensitive", "/private",
    "/restricted", "/internal", "/secret", "/hidden", "/exports", "/imports", "/downloads", "/attachments", "/backup_files", "/old_files",
    "/temp_files", "/drafts", "/staging_files", "/test_files", "/user_uploads", "/system_logs"
]

DIRECTORIES = list(dict.fromkeys(DIRECTORIES))

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
