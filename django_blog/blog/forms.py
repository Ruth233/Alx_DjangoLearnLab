from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Tag

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # author and published_date are handled automatically
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
 # comma-separated tags input (e.g. "django, python, tips")
        tags = forms.CharField(required=False, help_text="Comma-separated tags", widget=forms.TextInput(attrs={'placeholder': 'e.g. django, python'}))
            'tags': TagWidget(),
        }
        
class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment...'}),
        max_length=2000,
    )

    class Meta:
        model = Comment
        fields = ['content']


    def __init__(self, *args, **kwargs):
        # if instance passed, pre-fill tags as comma-separated string
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['tags'].initial = ', '.join([t.name for t in self.instance.tags.all()])

    def save(self, commit=True, author=None):
        """
        Save Post and tags. If author provided, set it before saving instance.
        """
        post = super().save(commit=False)
        if author and not post.pk:
            post.author = author
        if commit:
            post.save()
            # handle tags
            tags_str = self.cleaned_data.get('tags', '')
            tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
            # attach tags (create if necessary)
            post.tags.clear()
            for name in tag_names:
                tag_obj, _ = Tag.objects.get_or_create(name__iexact=name, defaults={'name': name})
                # get_or_create with case-insensitive check: use filter to be safe
                if not tag_obj:
                    tag_obj = Tag.objects.create(name=name)
                post.tags.add(tag_obj)
        return post

