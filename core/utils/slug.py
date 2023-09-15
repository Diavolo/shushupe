from nanoid import generate


def generate_slug() -> str:
    """Generate a slug using nanoid but without adding 'hyphen' (-)
    or "underscore" (_) at the beginning or at the end of that.

    Returns:
        str: slug
    """
    slug = generate()
    UNWANTED_CHAR = ['-', '_']
    while slug[0] in UNWANTED_CHAR or slug[-1] in UNWANTED_CHAR:
        slug = generate()
    return slug
