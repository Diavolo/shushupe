from decimal import Decimal


class ReviewType:
    ANIME = "Anime"  # Japanese-origin animated series (seasonal or long-running)
    BOOKS = "Books"  # Novels, non-fiction, short stories, essays, etc.
    COMICS_MANGA = "Comics/Manga"  # Comic books, graphic novels, manga, webtoons
    COURSES = "Courses"  # Online or in-person educational content
    EVENTS = "Events"  # Concerts, festivals, conferences, exhibitions
    GAMES = "Games"  # Video games, board games, card games, tabletop RPGs, etc.
    HOTELS = "Hotels"  # Hotels, hostels, resorts, and other accommodations
    MOVIES = "Movies"
    MUSIC = "Music"  # Albums, EPs, singles, soundtracks
    PODCASTS = "Podcasts"  # Audio or video podcast shows
    PRODUCTS = "Products"  # Physical goods not covered by other types (e.g. furniture, toys, hardware)
    RESTAURANTS = "Restaurants"
    SERIES = "Series"  # Episodic narrative content with seasons (TV, streaming, or web)
    SERVICES = (
        "Services"  # Services not covered by other types (e.g. utilities, telecoms)
    )
    SOFTWARE = "Software"  # Desktop apps, mobile apps, SaaS platforms, developer tools
    TV_SHOWS = "TV Shows"  # Non-serialized TV programs (news, talk shows, game shows)
    OTHER = "Other"  # Anything that doesn't fit the existing types

    REVIEW_TYPES = sorted(
        (
            (ANIME.lower(), ANIME.title()),
            (BOOKS.lower(), BOOKS.title()),
            (COMICS_MANGA.lower(), COMICS_MANGA.title()),
            (COURSES.lower(), COURSES.title()),
            (EVENTS.lower(), EVENTS.title()),
            (GAMES.lower(), GAMES.title()),
            (HOTELS.lower(), HOTELS.title()),
            (MOVIES.lower(), MOVIES.title()),
            (MUSIC.lower(), MUSIC.title()),
            (PODCASTS.lower(), PODCASTS.title()),
            (PRODUCTS.lower(), PRODUCTS.title()),
            (RESTAURANTS.lower(), RESTAURANTS.title()),
            (SERIES.lower(), SERIES.title()),
            (SERVICES.lower(), SERVICES.title()),
            (SOFTWARE.lower(), SOFTWARE.title()),
            (TV_SHOWS.lower(), TV_SHOWS),
            (OTHER.lower(), OTHER.title()),
        )
    )


class ReviewTopicType:
    ARTIST = "Artist"  # Musical artist or band
    AUTHOR = "Author"  # Writer or literary creator
    BRAND = "Brand"  # Commercial brand for products, software or services (e.g. Apple, Nike)
    CHAIN = "Chain"  # Physical location chain (e.g. restaurant, hotel, retail)
    COLLECTION = "Collection"  # Loose grouping of works without a narrative arc (e.g. discography, filmography)
    CREATOR = "Creator"  # Individual creator not covered by Artist or Author (e.g. director, podcaster, instructor)
    FRANCHISE = "Franchise"  # Commercial multimedia franchise (e.g. Star Wars, which spans films, games, books)
    SAGA = "Saga"  # Sequential narrative across multiple installments (e.g. Lord of the Rings)
    SERIES = "Series"  # Episodic show with seasons (TV, streaming, anime, podcast)
    STUDIO = "Studio"  # Production or development studio (e.g. Pixar, MAPPA, Rockstar)
    UNIVERSE = (
        "Universe"  # Shared fictional world across independent works (e.g. MCU, DC)
    )
    GENERAL = "General"

    REVIEW_TOPIC_TYPES = sorted(
        (
            (ARTIST.lower(), ARTIST.title()),
            (AUTHOR.lower(), AUTHOR.title()),
            (BRAND.lower(), BRAND.title()),
            (CHAIN.lower(), CHAIN.title()),
            (COLLECTION.lower(), COLLECTION.title()),
            (CREATOR.lower(), CREATOR.title()),
            (FRANCHISE.lower(), FRANCHISE.title()),
            (SAGA.lower(), SAGA.title()),
            (SERIES.lower(), SERIES.title()),
            (STUDIO.lower(), STUDIO.title()),
            (UNIVERSE.lower(), UNIVERSE.title()),
            (GENERAL.lower(), GENERAL.title()),
        )
    )


class RatingType:
    PESIMO = Decimal("1.0")
    MUY_DEFICIENTE = Decimal("1.5")
    DEFICIENTE = Decimal("2.0")
    POR_DEBAJO_DEL_PROMEDIO = Decimal("2.5")
    PROMEDIO = Decimal("3.0")
    LIGERAMENTE_SUPERIOR_AL_PROMEDIO = Decimal("3.5")
    BUENO = Decimal("4.0")
    MUY_BUENO = Decimal("4.5")
    EXCELENTE = Decimal("5.0")

    RATING_TYPES = sorted(
        (
            (Decimal("1.0"), f"{PESIMO} - Pésimo"),
            (Decimal("1.5"), f"{MUY_DEFICIENTE} - Muy deficiente"),
            (Decimal("2.0"), f"{DEFICIENTE} - Deficiente"),
            (Decimal("2.5"), f"{POR_DEBAJO_DEL_PROMEDIO} - Por debajo del promedio"),
            (Decimal("3.0"), f"{PROMEDIO} - Promedio"),
            (
                Decimal("3.5"),
                f"{LIGERAMENTE_SUPERIOR_AL_PROMEDIO} - Ligeramente superior al promedio",
            ),
            (Decimal("4.0"), f"{BUENO} - Bueno"),
            (Decimal("4.5"), f"{MUY_BUENO} - Muy bueno"),
            (Decimal("5.0"), f"{EXCELENTE} - Excelente"),
        )
    )


class CurrencyType:
    USD = "USD"  # US Dollar
    EUR = "EUR"  # Euro
    PEN = "PEN"  # Peruvian Sol
    ARS = "ARS"  # Argentine Peso
    AUD = "AUD"  # Australian Dollar
    BRL = "BRL"  # Brazilian Real
    CAD = "CAD"  # Canadian Dollar
    CLP = "CLP"  # Chilean Peso
    CNY = "CNY"  # Chinese Yuan
    COP = "COP"  # Colombian Peso
    GBP = "GBP"  # British Pound
    JPY = "JPY"  # Japanese Yen
    MXN = "MXN"  # Mexican Peso

    CURRENCY_TYPES = sorted(
        (
            (USD, "USD - US Dollar"),
            (EUR, "EUR - Euro"),
            (PEN, "PEN - Peruvian Sol"),
            (ARS, "ARS - Argentine Peso"),
            (AUD, "AUD - Australian Dollar"),
            (BRL, "BRL - Brazilian Real"),
            (CAD, "CAD - Canadian Dollar"),
            (CLP, "CLP - Chilean Peso"),
            (CNY, "CNY - Chinese Yuan"),
            (COP, "COP - Colombian Peso"),
            (GBP, "GBP - British Pound"),
            (JPY, "JPY - Japanese Yen"),
            (MXN, "MXN - Mexican Peso"),
        )
    )
