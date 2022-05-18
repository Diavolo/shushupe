from nanoid import generate


def generate_slug():
    slug = generate()
    while slug[0] == "-" or slug[-1] == "-" or "_" in slug:
        slug = generate()
    return slug
