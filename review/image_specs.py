from imagekit import ImageSpec, register
from imagekit.processors import SmartResize


@register.generator("review:review_landscape_image")
class ReviewLandscapeImage(ImageSpec):
    """Landscape 16:9 - 320x180"""

    processors = [SmartResize(320, 180)]
    format = "JPEG"
    options = {"quality": 85}


@register.generator("review:review_portrait_image")
class ReviewPortraitImage(ImageSpec):
    """Portrait 4:5 - 256x320"""

    processors = [SmartResize(256, 320)]
    format = "JPEG"
    options = {"quality": 85}


@register.generator("review:review_square_image")
class ReviewSquareImage(ImageSpec):
    """Square 1:1 - 320x320"""

    processors = [SmartResize(320, 320)]
    format = "JPEG"
    options = {"quality": 85}


@register.generator("review:review_tall_image")
class ReviewTallImage(ImageSpec):
    """Tall 9:16 - 180x320"""

    processors = [SmartResize(180, 320)]
    format = "JPEG"
    options = {"quality": 85}


# Other sizes


@register.generator("review:review_poster_image")
class ReviewPosterImage(ImageSpec):
    """Poster image - 260x370"""

    processors = [SmartResize(260, 370)]
    format = "JPEG"
    options = {"quality": 85}


@register.generator("review:review_small_landscape_image")
class ReviewSmallLandscapeImage(ImageSpec):
    """Small Landscape 16:9 - 160x90"""

    processors = [SmartResize(160, 90)]
    format = "JPEG"
    options = {"quality": 85}


@register.generator("review:review_small_tall_image")
class ReviewSmallTallImage(ImageSpec):
    """Small Tall 9:16 - 90x160"""

    processors = [SmartResize(90, 160)]
    format = "JPEG"
    options = {"quality": 85}
