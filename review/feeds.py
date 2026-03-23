from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from core.entry import Entry
from core.utils.constants import PASSWD_PROTECTED_MSG
from core.utils.post import get_full_path, RECENTLY
from core.utils.shushupe import SITE_NAME, SITE_URL


class LatestReviewsFeed(Feed):
    title = SITE_NAME
    link = "/"
    subtitle = "Latest reviews"
    feed_type = Atom1Feed
    feed_copyright = f"{SITE_NAME} - {SITE_URL}"

    def items(self):
        return Entry.get_published_review_list().select_related(
            "review_topic", "review_topic__parent"
        )[:RECENTLY]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        if item.protected_with_password:
            return PASSWD_PROTECTED_MSG
        return (
            f"<p>Rating: {item.rating}/5</p>"
            + item.content_html
            + get_full_path(item.get_absolute_url())
        )

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
