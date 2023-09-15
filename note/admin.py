from django import forms
from django.contrib import admin

from note.models import Note


class NoteForm(forms.ModelForm):
    """Custom validation form for NoteAdmin.

    - https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#adding-custom-validation-to-the-admin
    - https://docs.python.org/3/library/functions.html#super
    - https://stackoverflow.com/questions/1060281/in-django-admin-can-i-require-fields-in-a-model-but-not-when-it-is-inline

    Args:
        forms (_type_): _description_
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False


class NoteAdmin(admin.ModelAdmin):
    form = NoteForm
    exclude = ('author',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('content',)
    list_display = ('title', 'creation_date', 'pub_date', 'last_modified',
                    'status', 'is_public', 'protected_with_password', 'slug')
    list_filter = ('author', 'pub_date', 'status', 'tags')
    filter_horizontal = ('tags',)
    fieldsets = [
        ('Note info', {'fields': ['title', 'slug', 'content']}),
        ('Visibility', {'fields': ['is_public', 'status'],
                        'classes': ['collapse']}),
        ('Meta', {'fields': ['pub_date', 'allow_comments',
                             'protected_with_password', 'post_password'],
                  'classes': ['collapse']}),
        ('Taxonomy', {'fields': ['tags'], 'classes': ['collapse']})
    ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(NoteAdmin, self).save_model(request, obj, form, change)

    def post_url(self, obj):
        return obj.slug


admin.site.register(Note, NoteAdmin)
