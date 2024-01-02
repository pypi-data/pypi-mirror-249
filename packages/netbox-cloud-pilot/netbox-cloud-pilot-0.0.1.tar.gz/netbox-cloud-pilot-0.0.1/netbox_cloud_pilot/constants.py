from django import forms

from extras.constants import DEFAULT_DASHBOARD
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES
from .nb_settings import *

JELASTIC_API = "https://app.xapp.cloudmydc.com"
NETBOX_JPS_REPO = (
    "https://raw.githubusercontent.com/Onemind-Services-LLC/netbox-jps/master"
)
NODE_GROUP_CP = "cp"
NODE_GROUP_SQLDB = "sqldb"

SECTION_REQUIRED = None
SECTION_SYSTEM = "System"
SECTION_SECURITY = "Security"
SECTION_DATA = "Data"
SECTION_DEFAULT = "Default"
SECTION_DATETIME = "Date/Time"
SECTION_MISC = "Miscellaneous"
SECTION_DEVELOPMENT = "Development"
SECTION_CONTAINER = "Container"

NETBOX_SETTINGS = NbSettings(
    [
        NbSection(
            name=SECTION_REQUIRED,
            params=[
                Param(
                    key="ALLOWED_HOSTS",
                    label="Allowed Hosts",
                    help_text="Comma separated list of allowed hosts (FQDN, IP address, or pattern), or '*' for all",
                    placeholder="netbox.example.com, localhost",
                ),
                Param(
                    key="DB_CONN_MAX_AGE",
                    label="DB Connection Max Age",
                    help_text="Maximum age of database connections, in seconds",
                    placeholder="300",
                    required=False,
                    field_kwargs={"widget": forms.NumberInput(attrs={"min": 0})},
                ),
                Param(
                    key="DB_DISABLE_SERVER_SIDE_CURSORS",
                    label="DB Disable Server Side Cursors",
                    help_text="Disable server-side cursors",
                    required=False,
                    field=forms.ChoiceField,
                    field_kwargs={
                        "widget": forms.Select(),
                        "choices": BOOLEAN_WITH_BLANK_CHOICES,
                    },
                ),
                Param(
                    key="DB_HOST",
                    label="DB Host",
                    help_text="Database server hostname or IP address",
                    placeholder="localhost",
                ),
                Param(
                    key="DB_NAME",
                    label="DB Name",
                    help_text="Database name",
                    placeholder="netbox",
                ),
                Param(
                    key="DB_PASSWORD",
                    label="DB Password",
                    help_text="Database user password",
                    placeholder="password",
                ),
                Param(
                    key="DB_PORT",
                    label="DB Port",
                    help_text="Database server port",
                    placeholder="5432",
                    required=False,
                    field_kwargs={"widget": forms.NumberInput(attrs={"min": 0})},
                    initial=5432,
                ),
                Param(
                    key="DB_SSLMODE",
                    label="DB SSL Mode",
                    help_text="Database SSL mode",
                    required=False,
                    field=forms.ChoiceField,
                    field_kwargs={
                        "widget": forms.Select(),
                        "choices": [
                            ("disable", "Disable"),
                            ("allow", "Allow"),
                            ("prefer", "Prefer"),
                            ("require", "Require"),
                            ("verify-ca", "Verify CA"),
                            ("verify-full", "Verify Full"),
                        ],
                    },
                    initial="prefer",
                ),
                Param(
                    key="DB_USER",
                    label="DB User",
                    help_text="Database username",
                    placeholder="netbox",
                ),
                Param(
                    key="DB_WAIT_TIMEOUT",
                    label="DB Wait Timeout",
                    help_text="Database connection wait timeout, in seconds",
                    placeholder="300",
                    required=False,
                    field_kwargs={"widget": forms.NumberInput(attrs={"min": 0})},
                    initial=300,
                ),
                Param(
                    key="REDIS_HOST",
                    label="Redis Host",
                    help_text="Redis server hostname or IP address",
                    placeholder="redis",
                ),
                Param(
                    key="REDIS_INSECURE_SKIP_TLS_VERIFY",
                    label="Redis Insecure Skip TLS Verify",
                    help_text="Skip TLS verification when connecting to Redis",
                    required=False,
                    field=forms.ChoiceField,
                    field_kwargs={
                        "widget": forms.Select(),
                        "choices": BOOLEAN_WITH_BLANK_CHOICES,
                    },
                ),
                Param(
                    key="REDIS_PASSWORD",
                    label="Redis Password",
                    help_text="Redis server password",
                    placeholder="password",
                    required=False,
                ),
                Param(
                    key="REDIS_PORT",
                    label="Redis Port",
                    help_text="Redis server port",
                    placeholder="6379",
                    required=False,
                    field_kwargs={"widget": forms.NumberInput(attrs={"min": 0})},
                    initial=6379,
                ),
                Param(
                    key="REDIS_SSL",
                    label="Redis SSL",
                    help_text="Use SSL when connecting to Redis",
                    required=False,
                    field=forms.ChoiceField,
                    field_kwargs={
                        "widget": forms.Select(),
                        "choices": BOOLEAN_WITH_BLANK_CHOICES,
                    },
                ),
                Param(
                    key="REDIS_USERNAME",
                    label="Redis Username",
                    help_text="Redis server username",
                    placeholder="redis",
                    required=False,
                ),
            ],
        ),
        NbSection(
            name=SECTION_SYSTEM,
            params=[
                Param(
                    key="BASE_PATH",
                    label="Base Path",
                    help_text="Base path for URL patterns",
                    placeholder="/",
                    required=False,
                    initial="/",
                ),
                Param(
                    key="EMAIL_FROM",
                    label="Email From",
                    help_text="Default email sender address",
                    placeholder="NetBox <netbox@example.com>",
                    required=False,
                ),
                Param(
                    key="EMAIL_PASSWORD",
                    label="Email Password",
                    help_text="SMTP server password",
                    placeholder="password",
                    required=False,
                ),
                Param(
                    key="EMAIL_PORT",
                    label="Email Port",
                    help_text="SMTP server port",
                    placeholder="25",
                    required=False,
                    field_kwargs={"widget": forms.NumberInput(attrs={"min": 0})},
                ),
                Param(
                    key="EMAIL_SERVER",
                    label="Email Server",
                    help_text="SMTP server hostname or IP address",
                    placeholder="localhost",
                    required=False,
                ),
                Param(
                    key="EMAIL_SSL_CERTFILE",
                    label="Email SSL Certfile",
                    help_text="SMTP SSL certificate file",
                    placeholder="/path/to/certfile",
                    required=False,
                ),
                Param(
                    key="EMAIL_SSL_KEYFILE",
                    label="Email SSL Keyfile",
                    help_text="SMTP SSL key file",
                    placeholder="/path/to/keyfile",
                    required=False,
                ),
                Param(
                    key="EMAIL_TIMEOUT",
                    label="Email Timeout",
                    help_text="SMTP server timeout, in seconds",
                    placeholder="10",
                    required=False,
                    field_kwargs={"widget": forms.NumberInput(attrs={"min": 0})},
                ),
                Param(
                    key="EMAIL_USERNAME",
                    label="Email Username",
                    help_text="SMTP server username",
                    placeholder="admin@example.com",
                    required=False,
                    field_kwargs={"widget": forms.EmailInput()},
                ),
                Param(
                    key="EMAIL_USE_SSL",
                    label="Email Use SSL",
                    help_text="Use SSL when connecting to SMTP server",
                    required=False,
                    field=forms.ChoiceField,
                    field_kwargs={
                        "widget": forms.Select(),
                        "choices": BOOLEAN_WITH_BLANK_CHOICES,
                    },
                ),
                Param(
                    key="EMAIL_USE_TLS",
                    label="Email Use TLS",
                    help_text="Use TLS when connecting to SMTP server",
                    required=False,
                    field=forms.ChoiceField,
                    field_kwargs={
                        "widget": forms.Select(),
                        "choices": BOOLEAN_WITH_BLANK_CHOICES,
                    },
                ),
                Param(
                    key="ENABLE_LOCALIZATION",
                    label="Enable Localization",
                    required=False,
                    field=forms.ChoiceField,
                    field_kwargs={
                        "widget": forms.Select(),
                        "choices": BOOLEAN_WITH_BLANK_CHOICES,
                    },
                ),
                Param(
                    key="GIT_PATH",
                    label="Git Path",
                    help_text="Path to git executable",
                    placeholder="/usr/bin/git",
                    required=False,
                    initial="/usr/bin/git",
                ),
                Param(
                    key="HTTP_PROXIES",
                    label="HTTP Proxies",
                    help_text="Dictionary of HTTP proxies",
                    placeholder="{'http': 'http://proxy.example.com:3128'}",
                    required=False,
                ),
                Param(
                    key="INTERNAL_IPS",
                    label="Internal IPs",
                    help_text="List of internal IP addresses",
                    placeholder="127.0.0.1, ::1",
                    required=False,
                ),
                Param(
                    key="JINJA2_FILTERS",
                    label="Jinja2 Filters",
                    help_text="Dictionary of Jinja2 filters",
                    placeholder="{'filter_name': 'path.to.filter'}",
                    required=False,
                    field=forms.JSONField,
                    field_kwargs={
                        "widget": forms.Textarea(attrs={"class": "vLargeTextField"})
                    },
                    initial={},
                ),
                Param(
                    key="MEDIA_ROOT",
                    label="Media Root",
                    help_text="Absolute filesystem path to media files",
                    placeholder="/opt/netbox/netbox/media",
                    required=False,
                ),
                Param(
                    key="REPORTS_ROOT",
                    label="Reports Root",
                    help_text="Absolute filesystem path to reports",
                    placeholder="/opt/netbox/netbox/reports",
                    required=False,
                ),
                Param(
                    key="SCRIPTS_ROOT",
                    label="Scripts Root",
                    help_text="Absolute filesystem path to custom scripts",
                    placeholder="/opt/netbox/netbox/scripts",
                    required=False,
                ),
                Param(
                    key="STORAGE_BACKEND",
                    label="Storage Backend",
                    help_text="Storage backend for file attachments",
                    placeholder="django.core.files.storage.FileSystemStorage",
                    required=False,
                ),
                Param(
                    key="STORAGE_CONFIG",
                    label="Storage Config",
                    help_text="Configuration parameters for the storage backend",
                    placeholder="{'location': '/var/netbox/media'}",
                    required=False,
                    field=forms.JSONField,
                    field_kwargs={
                        "widget": forms.Textarea(attrs={"class": "vLargeTextField"})
                    },
                    initial={},
                ),
            ],
        ),
        NbSection(
            name=SECTION_SECURITY,
            params=[
                Param(
                    key="ALLOW_TOKEN_RETRIEVAL",
                    label="Allow Token Retrieval",
                    help_text="Allow retrieval of user tokens in API or UI",
                    required=False,
                    field=forms.ChoiceField,
                    field_kwargs={
                        "widget": forms.Select(),
                        "choices": BOOLEAN_WITH_BLANK_CHOICES,
                    },
                    initial=True,
                ),
                Param(
                    key="ALLOWED_URL_SCHEMES",
                    label="Allowed URL Schemes",
                    help_text="List of allowed URL schemes",
                    placeholder="http, https",
                    required=False,
                ),
                Param(
                    key="AUTH_PASSWORD_VALIDATORS",
                    label="Auth Password Validators",
                    help_text="List of password validators",
                    placeholder="[]",
                    required=False,
                    field=forms.JSONField,
                    field_kwargs={
                        "widget": forms.Textarea(attrs={"class": "vLargeTextField"})
                    },
                    initial=[
                        [
                            {
                                "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
                            },
                            {
                                "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
                                "OPTIONS": {
                                    "min_length": 10,
                                },
                            },
                            {
                                "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
                            },
                            {
                                "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
                            },
                        ]
                    ],
                ),
                Param(
                    key="CORS_ORIGIN_ALLOW_ALL",
                    label="CORS Origin Allow All",
                    help_text="Allow all CORS origins",
                    required=False,
                    field=forms.ChoiceField,
                    field_kwargs={
                        "widget": forms.Select(),
                        "choices": BOOLEAN_WITH_BLANK_CHOICES,
                    },
                ),
                Param(
                    key="CORS_ORIGIN_REGEX_WHITELIST",
                    label="CORS Origin Regex Whitelist",
                    help_text="List of CORS origin regex patterns",
                    placeholder="[]",
                    required=False,
                ),
                Param(
                    key="CORS_ORIGIN_WHITELIST",
                    label="CORS Origin Whitelist",
                    help_text="List of CORS origins",
                    placeholder="[]",
                    required=False,
                ),
                Param(
                    key="CSRF_COOKIE_NAME",
                    label="CSRF Cookie Name",
                    help_text="Name of the CSRF cookie",
                    placeholder="csrftoken",
                    required=False,
                    initial="csrftoken",
                ),
                Param(
                    key="CSRF_COOKIE_SECURE",
                    label="CSRF Cookie Secure",
                    help_text="Require HTTPS for CSRF cookie",
                    required=False,
                    field=forms.ChoiceField,
                    field_kwargs={
                        "widget": forms.Select(),
                        "choices": BOOLEAN_WITH_BLANK_CHOICES,
                    },
                ),
                Param(
                    key="CSRF_TRUSTED_ORIGINS",
                    label="CSRF Trusted Origins",
                    help_text="List of trusted origins for CSRF",
                    placeholder="[]",
                    required=False,
                ),
                Param(
                    key="LOGIN_PERSISTENCE",
                    label="Login Persistence",
                    help_text="Enable session persistence after browser restart",
                    required=False,
                    field=forms.ChoiceField,
                    field_kwargs={
                        "widget": forms.Select(),
                        "choices": BOOLEAN_WITH_BLANK_CHOICES,
                    },
                    initial=True,
                ),
                Param(
                    key="LOGIN_REQUIRED",
                    label="Login Required",
                    help_text="Require authentication to access any data",
                    required=False,
                    field=forms.ChoiceField,
                    field_kwargs={
                        "widget": forms.Select(),
                        "choices": BOOLEAN_WITH_BLANK_CHOICES,
                    },
                ),
                Param(
                    key="LOGIN_TIMEOUT",
                    label="Login Timeout",
                    help_text="Session timeout, in seconds",
                    placeholder="1209600",
                    required=False,
                    field_kwargs={"widget": forms.NumberInput(attrs={"min": 0})},
                    initial=1209600,
                ),
                Param(
                    key="SECURE_SSL_REDIRECT",
                    label="Secure SSL Redirect",
                    help_text="Redirect all non-HTTPS requests to HTTPS",
                    required=False,
                    field=forms.ChoiceField,
                    field_kwargs={
                        "widget": forms.Select(),
                        "choices": BOOLEAN_WITH_BLANK_CHOICES,
                    },
                ),
            ],
        ),
        NbSection(
            name=SECTION_DATA,
            params=[
                Param(
                    key="CUSTOM_VALIDATORS",
                    label="Custom Validators",
                    help_text="List of custom data validators",
                    placeholder="[]",
                    required=False,
                    field_kwargs={
                        "widget": forms.Textarea(attrs={"class": "vLargeTextField"})
                    },
                ),
                Param(
                    key="FIELD_CHOICES",
                    label="Field Choices",
                    help_text="List of custom field choices",
                    placeholder="[]",
                    required=False,
                    field_kwargs={
                        "widget": forms.Textarea(attrs={"class": "vLargeTextField"})
                    },
                ),
            ],
        ),
        NbSection(
            name=SECTION_DEFAULT,
            params=[
                Param(
                    key="DEFAULT_DASHBOARD",
                    label="Default Dashboard",
                    help_text="Default dashboard for users",
                    required=False,
                    field=forms.JSONField,
                    field_kwargs={
                        "widget": forms.Textarea(attrs={"class": "vLargeTextField"})
                    },
                    initial=DEFAULT_DASHBOARD,
                ),
                Param(
                    key="DEFAULT_USER_PREFERENCES",
                    label="Default User Preferences",
                    help_text="Default user preferences",
                    required=False,
                    field=forms.JSONField,
                    field_kwargs={
                        "widget": forms.Textarea(attrs={"class": "vLargeTextField"})
                    },
                    initial={},
                ),
                Param(
                    key="PAGINATE_COUNT",
                    label="Paginate Count",
                    help_text="Default number of objects to display per page",
                    placeholder="50",
                    required=False,
                    field_kwargs={"widget": forms.NumberInput(attrs={"min": 1})},
                ),
                Param(
                    key="POWERFEED_DEFAULT_AMPERAGE",
                    label="Powerfeed Default Amperage",
                    help_text="Default power feed amperage",
                    placeholder="20",
                    required=False,
                    field_kwargs={"widget": forms.NumberInput(attrs={"min": 0})},
                ),
                Param(
                    key="POWERFEED_DEFAULT_MAX_UTILIZATION",
                    label="Powerfeed Default Max Utilization",
                    help_text="Default power feed maximum utilization",
                    placeholder="80",
                    required=False,
                    field_kwargs={"widget": forms.NumberInput(attrs={"min": 0})},
                ),
                Param(
                    key="POWERFEED_DEFAULT_VOLTAGE",
                    label="Powerfeed Default Voltage",
                    help_text="Default power feed voltage",
                    placeholder="120",
                    required=False,
                    field_kwargs={"widget": forms.NumberInput(attrs={"min": 0})},
                ),
                Param(
                    key="RACK_ELEVATION_DEFAULT_UNIT_HEIGHT",
                    label="Rack Elevation Default Unit Height",
                    help_text="Default rack elevation unit height",
                    placeholder="44",
                    required=False,
                    field_kwargs={"widget": forms.NumberInput(attrs={"min": 0})},
                ),
                Param(
                    key="RACK_ELEVATION_DEFAULT_UNIT_WIDTH",
                    label="Rack Elevation Default Unit Width",
                    help_text="Default rack elevation unit width",
                    placeholder="50",
                    required=False,
                    field_kwargs={"widget": forms.NumberInput(attrs={"min": 0})},
                ),
            ],
        ),
        NbSection(
            name=SECTION_DATETIME,
            params=[
                Param(
                    key="DATETIME_FORMAT",
                    label="Datetime Format",
                    help_text="Default datetime format",
                    placeholder="N j, Y, H:i:s T",
                    required=False,
                ),
                Param(
                    key="DATE_FORMAT",
                    label="Date Format",
                    help_text="Default date format",
                    placeholder="N j, Y",
                    required=False,
                ),
                Param(
                    key="SHORT_DATETIME_FORMAT",
                    label="Short Datetime Format",
                    help_text="Default short datetime format",
                    placeholder="m/d/Y P",
                    required=False,
                ),
                Param(
                    key="SHORT_DATE_FORMAT",
                    label="Short Date Format",
                    help_text="Default short date format",
                    placeholder="m/d/Y",
                    required=False,
                ),
                Param(
                    key="SHORT_TIME_FORMAT",
                    label="Short Time Format",
                    help_text="Default short time format",
                    placeholder="H:i:s",
                    required=False,
                ),
                Param(
                    key="TIME_FORMAT",
                    label="Time Format",
                    help_text="Default time format",
                    placeholder="H:i:s",
                    required=False,
                ),
                Param(
                    key="TIME_ZONE",
                    label="Time Zone",
                    help_text="Default time zone",
                    placeholder="UTC",
                    required=False,
                ),
            ],
        ),
        NbSection(
            name=SECTION_MISC,
            params=[
                Param(
                    key="ADMINS",
                    label="Admins",
                    help_text="List of NetBox administrators",
                    placeholder="[('NetBox Admin', 'admin@example.com')]",
                    required=False,
                    field_kwargs={
                        "widget": forms.Textarea(attrs={"class": "vLargeTextField"})
                    },
                ),
                Param(
                    key="BANNER_BOTTOM",
                    label="Banner Bottom",
                    help_text="Bottom banner text",
                    placeholder="Banner text",
                    required=False,
                    field_kwargs={
                        "widget": forms.Textarea(attrs={"class": "vLargeTextField"})
                    },
                ),
                Param(
                    key="BANNER_LOGIN",
                    label="Banner Login",
                    help_text="Login banner text",
                    placeholder="Banner text",
                    required=False,
                    field_kwargs={
                        "widget": forms.Textarea(attrs={"class": "vLargeTextField"})
                    },
                ),
                Param(
                    key="BANNER_TOP",
                    label="Banner Top",
                    help_text="Top banner text",
                    placeholder="Banner text",
                    required=False,
                    field_kwargs={
                        "widget": forms.Textarea(attrs={"class": "vLargeTextField"})
                    },
                ),
                Param(
                    key="BANNER_MAINTENANCE",
                    label="Banner Maintenance",
                    help_text="Maintenance banner text",
                    placeholder="Banner text",
                    required=False,
                    field_kwargs={
                        "widget": forms.Textarea(attrs={"class": "vLargeTextField"})
                    },
                ),
                Param(
                    key="CENSUS_REPORTING_ENABLED",
                    label="Census Reporting Enabled",
                    help_text="Enable census reporting",
                    required=False,
                    field=forms.ChoiceField,
                    field_kwargs={
                        "widget": forms.Select(),
                        "choices": BOOLEAN_WITH_BLANK_CHOICES,
                    },
                ),
                Param(
                    key="CHANGELOG_RETENTION",
                    label="Changelog Retention",
                    help_text="Change log retention policy, in days",
                    placeholder="90",
                    required=False,
                    field_kwargs={"widget": forms.NumberInput(attrs={"min": 0})},
                ),
                Param(
                    key="DATA_UPLOAD_MAX_MEMORY_SIZE",
                    label="Data Upload Max Memory Size",
                    help_text="Maximum size of file uploads, in bytes",
                    placeholder="2621440",
                    required=False,
                    field_kwargs={"widget": forms.NumberInput(attrs={"min": 0})},
                ),
                Param(
                    key="ENFORCE_GLOBAL_UNIQUE",
                    label="Enforce Global Unique",
                    help_text="Enforce global uniqueness of IP addresses",
                    placeholder="False",
                    required=False,
                    field=forms.ChoiceField,
                    field_kwargs={
                        "widget": forms.Select(),
                        "choices": BOOLEAN_WITH_BLANK_CHOICES,
                    },
                ),
                Param(
                    key="FILE_UPLOAD_MAX_MEMORY_SIZE",
                    label="File Upload Max Memory Size",
                    help_text="Maximum size of file uploads, in bytes",
                    placeholder="2621440",
                    required=False,
                    field_kwargs={"widget": forms.NumberInput(attrs={"min": 0})},
                ),
                Param(
                    key="GRAPHQL_ENABLED",
                    label="GraphQL Enabled",
                    help_text="Enable GraphQL API",
                    placeholder="False",
                    required=False,
                    field=forms.ChoiceField,
                    field_kwargs={
                        "widget": forms.Select(),
                        "choices": BOOLEAN_WITH_BLANK_CHOICES,
                    },
                ),
                Param(
                    key="JOB_RETENTION",
                    label="Job Retention",
                    help_text="Job retention policy, in days",
                    placeholder="365",
                    required=False,
                    field_kwargs={"widget": forms.NumberInput(attrs={"min": 0})},
                ),
                Param(
                    key="MAINTENANCE_MODE",
                    label="Maintenance Mode",
                    help_text="Enable maintenance mode",
                    placeholder="False",
                    required=False,
                    field=forms.ChoiceField,
                    field_kwargs={
                        "widget": forms.Select(),
                        "choices": BOOLEAN_WITH_BLANK_CHOICES,
                    },
                ),
                Param(
                    key="MAPS_URL",
                    label="Maps URL",
                    help_text="URL to link to external maps",
                    placeholder="https://maps.google.com/?q=",
                    required=False,
                    field=forms.URLField,
                ),
                Param(
                    key="MAX_PAGE_SIZE",
                    label="Max Page Size",
                    help_text="Maximum page size for paginated results",
                    placeholder="1000",
                    required=False,
                    field_kwargs={"widget": forms.NumberInput(attrs={"min": 1})},
                ),
                Param(
                    key="METRICS_ENABLED",
                    label="Metrics Enabled",
                    help_text="Enable metrics reporting",
                    required=False,
                    field=forms.ChoiceField,
                    field_kwargs={
                        "widget": forms.Select(),
                        "choices": BOOLEAN_WITH_BLANK_CHOICES,
                    },
                ),
                Param(
                    key="PREFER_IPV4",
                    label="Prefer IPv4",
                    help_text="Prefer IPv4 addresses over IPv6",
                    required=False,
                    field=forms.ChoiceField,
                    field_kwargs={
                        "widget": forms.Select(),
                        "choices": BOOLEAN_WITH_BLANK_CHOICES,
                    },
                ),
                Param(
                    key="QUEUE_MAPPINGS",
                    label="Queue Mappings",
                    help_text="Dictionary of queue mappings",
                    placeholder="{'queue_name': 'queue_name'}",
                    required=False,
                    field=forms.JSONField,
                    field_kwargs={
                        "widget": forms.Textarea(attrs={"class": "vLargeTextField"})
                    },
                ),
                Param(
                    key="RELEASE_CHECK_URL",
                    label="Release Check URL",
                    help_text="URL for release check",
                    placeholder="https://api.github.com/repos/netbox-community/netbox/releases",
                    required=False,
                    field=forms.URLField,
                ),
                Param(
                    key="RQ_DEFAULT_TIMEOUT",
                    label="RQ Default Timeout",
                    help_text="Default timeout for RQ jobs, in seconds",
                    placeholder="300",
                    required=False,
                    field_kwargs={"widget": forms.NumberInput(attrs={"min": 1})},
                ),
                Param(
                    key="RQ_RETRY_INTERVAL",
                    label="RQ Retry Interval",
                    help_text="Interval between RQ job retries, in seconds",
                    placeholder="60",
                    required=False,
                    field_kwargs={"widget": forms.NumberInput(attrs={"min": 1})},
                ),
                Param(
                    key="RQ_RETRY_MAX",
                    label="RQ Retry Max",
                    help_text="Maximum number of RQ job retries",
                    placeholder="3",
                    required=False,
                    field_kwargs={"widget": forms.NumberInput(attrs={"min": 0})},
                ),
            ],
        ),
        NbSection(
            name=SECTION_DEVELOPMENT,
            params=[
                Param(
                    key="DEBUG",
                    label="Debug",
                    help_text="Enable debugging mode",
                    required=False,
                    field=forms.ChoiceField,
                    field_kwargs={
                        "widget": forms.Select(),
                        "choices": BOOLEAN_WITH_BLANK_CHOICES,
                    },
                ),
                Param(
                    key="DEVELOPER",
                    label="Developer",
                    help_text="Enable developer mode, use with caution",
                    required=False,
                    field=forms.ChoiceField,
                    field_kwargs={
                        "widget": forms.Select(),
                        "choices": BOOLEAN_WITH_BLANK_CHOICES,
                    },
                ),
            ],
        ),
        NbSection(
            name=SECTION_CONTAINER,
            params=[
                Param(
                    key="HOUSEKEEPING_INTERVAL",
                    label="Housekeeping Interval",
                    help_text="Interval between housekeeping tasks, in seconds",
                    placeholder="3600",
                    required=False,
                    field_kwargs={"widget": forms.NumberInput(attrs={"min": 10})},
                ),
                Param(
                    key="LOGLEVEL",
                    label="Loglevel",
                    help_text="Log level",
                    placeholder="INFO",
                    required=False,
                    field=forms.ChoiceField,
                    field_kwargs={
                        "widget": forms.Select(),
                        "choices": [
                            ("DEBUG", "DEBUG"),
                            ("INFO", "INFO"),
                            ("WARNING", "WARNING"),
                            ("ERROR", "ERROR"),
                            ("CRITICAL", "CRITICAL"),
                        ],
                    },
                ),
                Param(
                    key="MAX_DB_WAIT_TIME",
                    label="Max DB Wait Time",
                    help_text="Maximum time to wait for database, in seconds",
                    placeholder="300",
                    required=False,
                    field_kwargs={"widget": forms.NumberInput(attrs={"min": 1})},
                ),
            ],
        ),
    ]
)

NETBOX_SUPERUSER_SETTINGS = ["SUPERUSER_NAME", "SUPERUSER_EMAIL", "SUPERUSER_PASSWORD"]
