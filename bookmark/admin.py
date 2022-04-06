from django.contrib import admin

from bookmark.models import Bookmark


class BookmarkAdmin(admin.ModelAdmin):
    exclude = ('author', 'slug')
    search_fields = ('site_url',)
    list_display = ('title', 'creation_date', 'pub_date', 'last_modified',
                    'status', 'is_public', 'protected_with_password', 'slug')
    list_filter = ('author', 'pub_date', 'status', 'tags')
    filter_horizontal = ('tags',)
    fieldsets = [
        ('Article info', {'fields': ['title', 'site_url', 'content']}),
        ('Visibility', {'fields': ['is_public', 'status'],
                        'classes': ['collapse']}),
        ('Meta', {'fields': ['pub_date', 'allow_comments',
                             'protected_with_password', 'post_password'],
                  'classes': ['collapse']}),
        ('Taxonomy', {'fields': ['tags', ]})
    ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(BookmarkAdmin, self).save_model(request, obj, form, change)

    def post_url(self, obj):
        return obj.slug


admin.site.register(Bookmark, BookmarkAdmin)
