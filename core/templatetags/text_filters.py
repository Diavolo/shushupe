from django import template


register = template.Library()


@register.filter(name="snake_to_spaces")
def snake_to_spaces(value: str) -> str:
    """Unsnake a string.

    Args:
        value (str): The string to unsnake.

    Returns:
        str: The unsnake string.
    """
    if not value:
        return ""
    return str(value).replace("_", " ")
