from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "subtitle",
            "summary",
            "genre",
            "isbn",
            "pages",
            "language",
            "publication_date",
        ]



class BookSearchForm(forms.Form):
    q = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={"placeholder": "Search title, author or ISBN"}))
    genre = forms.ChoiceField(required=False, choices=[("", "All Genres")] + list(Book.GENRE_CHOICES))
    sort = forms.ChoiceField(required=False, choices=[("title", "Title A-Z"), ("-title", "Title Z-A"), ("-rating", "Highest rated"), ("-publication_date", "Newest"), ("publication_date", "Oldest")])


# registration form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
         raise forms.ValidationError(
            "An account with this email address already exists."
        )
        return email