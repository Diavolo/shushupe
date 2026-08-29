SECTION_READING = "Reading"
SECTION_WATCHING = "Watching"
SECTION_LISTENING = "Listening"
SECTION_PLAYING = "Playing"
SECTION_LEARNING = "Learning"

READING_TYPES = {"article", "book", "comic_manga", "paper"}
WATCHING_TYPES = {"movie", "series", "tv_show", "video"}
LISTENING_TYPES = {"album", "podcast", "single", "track"}
PLAYING_TYPES = {"game"}
LEARNING_TYPES = {"course"}

# Playlist appears in Listening or Watching depending on format.
PLAYLIST_TYPE = "playlist"
PLAYLIST_LISTENING_FORMATS = {
    "apple_music",
    "bandcamp",
    "deezer",
    "spotify",
    "tidal",
    "youtube_music",
}
PLAYLIST_WATCHING_FORMATS = {
    "vimeo",
    "youtube",
}

TYPE_TO_SECTION = {
    "album": SECTION_LISTENING,
    "article": SECTION_READING,
    "book": SECTION_READING,
    "comic_manga": SECTION_READING,
    "course": SECTION_LEARNING,
    "game": SECTION_PLAYING,
    "movie": SECTION_WATCHING,
    "paper": SECTION_READING,
    "podcast": SECTION_LISTENING,
    "series": SECTION_WATCHING,
    "single": SECTION_LISTENING,
    "track": SECTION_LISTENING,
    "tv_show": SECTION_WATCHING,
    "video": SECTION_WATCHING,
}

TYPE_FORMATS = {
    "album": (
        ("cassette", "Cassette"),
        ("cd", "CD"),
        ("digital_download", "Digital download"),
        ("streaming", "Streaming"),
        ("vinyl", "Vinyl"),
    ),
    "article": (
        ("newsletter", "Newsletter"),
        ("pdf", "PDF"),
        ("print", "Print"),
        ("web", "Web"),
    ),
    "book": (
        ("audiobook", "Audiobook"),
        ("ebook", "Ebook"),
        ("hardcover", "Hardcover"),
        ("paperback", "Paperback"),
    ),
    "comic_manga": (
        ("digital", "Digital"),
        ("print", "Print"),
        ("trade_paperback", "Trade paperback"),
        ("webtoon", "Webtoon"),
    ),
    "course": (
        ("book", "Book"),
        ("hybrid", "Hybrid"),
        ("in_person", "In person"),
        ("online", "Online"),
    ),
    "game": (
        ("console", "Console"),
        ("handheld", "Handheld"),
        ("mobile", "Mobile"),
        ("pc", "PC"),
        ("tabletop", "Tabletop"),
    ),
    "movie": (
        ("blu_ray", "Blu-ray"),
        ("cinema", "Cinema"),
        ("digital_rental", "Digital rental"),
        ("dvd", "DVD"),
        ("streaming", "Streaming"),
        ("tv_broadcast", "TV broadcast"),
    ),
    "paper": (
        ("pdf", "PDF"),
        ("preprint", "Preprint"),  # arXiv, bioRxiv, etc.
        ("print", "Print"),
        ("web", "Web"),  # DOI, publisher online, etc.
    ),
    "playlist": (
        ("apple_music", "Apple Music"),
        ("bandcamp", "Bandcamp"),
        ("deezer", "Deezer"),
        ("spotify", "Spotify"),
        ("tidal", "Tidal"),
        ("vimeo", "Vimeo"),
        ("youtube", "YouTube"),
        ("youtube_music", "YouTube Music"),
    ),
    "podcast": (
        ("apple_podcasts", "Apple Podcasts"),
        ("radio", "Radio"),
        ("rss", "RSS"),
        ("spotify", "Spotify"),
        ("youtube", "YouTube"),
    ),
    "series": (
        ("blu_ray", "Blu-ray"),
        ("broadcast", "Broadcast"),
        ("digital", "Digital"),
        ("dvd", "DVD"),
        ("streaming", "Streaming"),
    ),
    "single": (
        ("cassette", "Cassette"),
        ("cd", "CD"),
        ("digital_download", "Digital download"),
        ("streaming", "Streaming"),
        ("vinyl", "Vinyl"),
    ),
    "track": (
        ("cassette", "Cassette"),
        ("cd", "CD"),
        ("digital_download", "Digital download"),
        ("radio", "Radio"),
        ("streaming", "Streaming"),
        ("vinyl", "Vinyl"),
    ),
    "tv_show": (
        ("blu_ray", "Blu-ray"),
        ("broadcast", "Broadcast"),
        ("digital", "Digital"),
        ("dvd", "DVD"),
        ("streaming", "Streaming"),
    ),
    "video": (
        ("download", "Download"),
        ("stream", "Stream"),
        ("vimeo", "Vimeo"),
        ("youtube", "YouTube"),
    ),
}

FORMAT_VALUES_BY_TYPE = {
    consumption_type: {value for value, _ in formats}
    for consumption_type, formats in TYPE_FORMATS.items()
}

ALL_FORMAT_CHOICES = tuple(
    sorted(
        {
            (value, label)
            for formats in TYPE_FORMATS.values()
            for value, label in formats
        },
        key=lambda choice: choice[1].lower(),
    )
)

CONSUMPTION_TYPE_LABELS = {
    "album": "Album",
    "article": "Article",
    "book": "Book",
    "comic_manga": "Comic/Manga",
    "course": "Course",
    "game": "Game",
    "movie": "Movie",
    "paper": "Paper",
    "playlist": "Playlist",
    "podcast": "Podcast",
    "series": "Series",
    "single": "Single",
    "track": "Track",
    "tv_show": "TV Show",
    "video": "Video",
}

GROUPED_FORMAT_CHOICES = [("", "---------")] + [
    (CONSUMPTION_TYPE_LABELS[consumption_type], list(TYPE_FORMATS[consumption_type]))
    for consumption_type in sorted(
        TYPE_FORMATS,
        key=lambda key: CONSUMPTION_TYPE_LABELS[key].lower(),
    )
]

PAPER_TYPE = "paper"
PAPER_URL_REQUIRED_FORMATS = {"preprint", "web"}

SECTION_TO_DETAIL_URL = {
    SECTION_READING: "consumption:reading-detail",
    SECTION_WATCHING: "consumption:watching-detail",
    SECTION_LISTENING: "consumption:listening-detail",
    SECTION_PLAYING: "consumption:playing-detail",
    SECTION_LEARNING: "consumption:learning-detail",
}

SECTION_TO_LIST_URL = {
    SECTION_READING: "consumption:reading-list",
    SECTION_WATCHING: "consumption:watching-list",
    SECTION_LISTENING: "consumption:listening-list",
    SECTION_PLAYING: "consumption:playing-list",
    SECTION_LEARNING: "consumption:learning-list",
}

SECTION_TO_FEED_URL = {
    SECTION_READING: "consumption:reading-feed",
    SECTION_WATCHING: "consumption:watching-feed",
    SECTION_LISTENING: "consumption:listening-feed",
    SECTION_PLAYING: "consumption:playing-feed",
    SECTION_LEARNING: "consumption:learning-feed",
}


def section_for(consumption_type, format=""):
    """Return the section for a consumption type and optional format."""
    if consumption_type == PLAYLIST_TYPE:
        if format in PLAYLIST_LISTENING_FORMATS:
            return SECTION_LISTENING
        if format in PLAYLIST_WATCHING_FORMATS:
            return SECTION_WATCHING
        return None
    return TYPE_TO_SECTION.get(consumption_type)


def requires_url(consumption_type: str, format: str = "", url: str = "") -> bool:
    """Return True if the consumption type and format requires a URL, False otherwise."""
    return (
        consumption_type == PAPER_TYPE
        and format in PAPER_URL_REQUIRED_FORMATS
        and not url
    )
