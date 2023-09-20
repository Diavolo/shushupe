from bs4 import BeautifulSoup
from django.conf import settings

RECENTLY = 5
_site_url = settings.SITE_URL


class PostType:
    ARTICLE = 'Article'
    NOTE = 'Note'
    PAGE = 'Page'
    BOOKMARK = 'Bookmark'
    CHANGELOG = 'Changelog'

    POST_TYPES = sorted(((ARTICLE.lower(), ARTICLE.title()),
                         (NOTE.lower(), NOTE.title()),
                         (PAGE.lower(), PAGE.title())))


class PostStatus:
    PUBLISHED = 'published'
    DRAFT = 'draft'

    POST_STATUSES = sorted(((PUBLISHED.lower(), PUBLISHED.title()),
                            (DRAFT.lower(), DRAFT.title())))


def get_full_path(item_url: str) -> str:
    """Get the complete path of an 'item'.

    Args:
        item_url (str): Item URL (i.e. /about/) without the base name.

    Returns:
        str: Full path of the item (including the base URL i.e. https://...)
    """
    return f"{_site_url}{item_url}"


def truncate_html(html_content, max_length):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize the truncated content
    truncated_content = []

    # Initialize a variable to keep track of the current content length
    current_length = 0

    # Iterate through the HTML elements
    for element in soup.recursiveChildGenerator():
        # If the element is a string (text), calculate its length and add it to the truncated content
        if isinstance(element, str):
            text = str(element)
            current_length += len(text)

            # If the current length exceeds the maximum length, truncate the text
            if current_length > max_length:
                # remaining_length = max_length - (current_length - len(text))
                # truncated_text = text[:remaining_length]
                # truncated_content.append(truncated_text)
                break
            else:
                truncated_content.append(text)
        else:
            # For non-text elements (tags), add them to the truncated content
            truncated_content.append(str(element))

    # Join the truncated content to form the final HTML
    truncated_html = ''.join(truncated_content)

    return truncated_html
