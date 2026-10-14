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
