from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed

from consumption.constants import (
    SECTION_LEARNING,
    SECTION_LISTENING,
    SECTION_PLAYING,
    SECTION_READING,
    SECTION_TO_LIST_URL,
    SECTION_WATCHING,
)
from consumption.querysets import public_consumptions_for_section
from core.utils.constants import PASSWD_PROTECTED_MSG
from core.utils.post import RECENTLY, get_full_path
from core.utils.shushupe import SITE_NAME, SITE_URL


class ConsumptionSectionFeed(Feed):
    section = None
    feed_type = Atom1Feed
    feed_copyright = f"{SITE_NAME} - {SITE_URL}"

    def title(self):
        return f"{SITE_NAME}: {self.section}"

    def subtitle(self):
        return f"Latest {self.section.lower()}"

    def link(self):
        return reverse(SECTION_TO_LIST_URL[self.section])

    def items(self):
        return public_consumptions_for_section(self.section)[:RECENTLY]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        if item.protected_with_password:
            return PASSWD_PROTECTED_MSG
        return item.content_html + get_full_path(item.get_absolute_url())

    def item_pubdate(self, item):
        return item.pub_date

    def item_updateddate(self, item):
        return item.last_modified

    def item_author_name(self, item):
        return item.author.first_name

    def item_author_link(self):
        return SITE_URL

    def item_copyright(self):
        return self.feed_copyright


class LearningFeed(ConsumptionSectionFeed):
    section = SECTION_LEARNING


class ListeningFeed(ConsumptionSectionFeed):
    section = SECTION_LISTENING


class PlayingFeed(ConsumptionSectionFeed):
    section = SECTION_PLAYING


class ReadingFeed(ConsumptionSectionFeed):
    section = SECTION_READING


class WatchingFeed(ConsumptionSectionFeed):
    section = SECTION_WATCHING
