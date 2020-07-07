from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """
    # post = forms.IntegerField()
     author = forms.CharField(label="Nombre *", max_length=60,
                              widget=forms.TextInput(
                                  attrs={'placeholder': 'Nombre'}))
     author_email = forms.EmailField(label="E-mail *", max_length=100,
                                     widget=forms.EmailInput(
                                         attrs={'placeholder': 'E-mail'}))
     author_url = forms.URLField(label="URL", max_length=200,
                                 widget=forms.URLInput(
                                     attrs={'placeholder': 'URL',
                                            'required': False}))
    # author_ip = forms.GenericIPAddressField(protocol='both', unpack_ipv4=True)
    # comment_date = forms.DateTimeField()
     title = forms.CharField(label="Título", max_length=200,
                             widget=forms.TextInput(
                                 attrs={'placeholder': 'Título',
                                        'required': False}))
     content = forms.CharField(label="Comentario *", widget=forms.Textarea(
                                     attrs={'placeholder': 'Comentario'}))
    # karma = forms.IntegerField()
    # approved = forms.BooleanField()
    # comment_parent = forms.IntegerField()
    # user = forms.IntegerField()
    """

    class Meta:
        model = Comment
        fields = ['author', 'author_email', 'author_url', 'title', 'content']
        labels = {
            'author': 'Nombre*',
            'author_email': 'E-mail*',
            'author_url': 'URL',
            'title': 'Título',
            'content': 'Comentario*'
        }

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('kwargs', kwargs)
        # if (self.request.user.username):
        #     pass
    """


class LoggedCommentForm(forms.ModelForm):
    """Form for authenticated user"""
    class Meta:
        model = Comment
        fields = ['title', 'content']
        labels = {
            'title': 'Título',
            'content': 'Comentario'
        }
