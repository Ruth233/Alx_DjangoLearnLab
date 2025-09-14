# LibraryProject/bookshelf/forms.py
from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Book

User = get_user_model()


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author"]
        widgets = {
            "title": forms.TextInput(attrs={"maxlength": 200}),
            "author": forms.TextInput(attrs={"maxlength": 100}),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title", "").strip()
        # Simple sanitization: trim and remove control characters
        return "".join(ch for ch in title if ch.isprintable())


class SearchForm(forms.Form):
    q = forms.CharField(max_length=200, required=False, label="Search")

    def clean_q(self):
        q = self.cleaned_data.get("q", "").strip()
        # Return sanitized query; ORM will use this safely (no raw SQL)
        return q


class CustomUserCreationForm(UserCreationForm):
    """
    Extends built-in UserCreationForm to optionally capture
    date_of_birth and profile_photo (works if your custom user model has them).
    """
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    profile_photo = forms.ImageField(required=False)

    class Meta:
        model = User
        # order fields as you want them to appear in template
        fields = ("username", "email", "date_of_birth", "profile_photo", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        # Only set these if the User model has these attributes
        dob = self.cleaned_data.get("date_of_birth")
        photo = self.cleaned_data.get("profile_photo")
        if dob is not None and hasattr(user, "date_of_birth"):
            user.date_of_birth = dob
        if commit:
            user.save()
            if photo is not None and hasattr(user, "profile_photo"):
                user.profile_photo = photo
                user.save()
        return user
