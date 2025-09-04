import attila

AUTHOR = 'Newton Miyoshi'
SITENAME = 'Cafezando'
SITEURL = "http://localhost:3000"

PATH = "content"

TIMEZONE = 'America/Sao_Paulo'

DEFAULT_LANG = 'pt'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

THEME = attila.get_path()

HOME_COVER = 'images/cover.png'

# Plugins
PLUGINS = [
    "image_process",
    "seo",
]

# Image Process configuration to support classes like image-process-large-photo
IMAGE_PROCESS = {
    "large-photo": {
        "type": "responsive-image",
        "sizes": (
            "(min-width: 1200px) 800px, "
            "(min-width: 992px) 650px, "
            "(min-width: 768px) 718px, "
            "100vw"
        ),
        "srcset": [
            ("600w", ["scale_in 600 450 True"]),
            ("800w", ["scale_in 800 600 True"]),
            ("1600w", ["scale_in 1600 1200 True"]),
        ],
        "default": "800w",
    }
}

# Optional: where to store derivatives (default is 'derivative')
# IMAGE_PROCESS_DIR = "derivative"