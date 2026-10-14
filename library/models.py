from django.db import models
from django.core.validators import (
    MinLengthValidator,
    MinValueValidator,
    MaxValueValidator,
)


class Author(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)]
    )
    bio = models.TextField(blank=True, null=True)
    country = models.CharField(
        max_length=50,
        default="South Africa"
    )

    class Meta:
        ordering = ["name"]

    def short_bio(self):
        if self.bio:
            return self.bio[:50] + (
                "..." if len(self.bio) > 50 else ""
            )
        return "No biography available."

    def __str__(self):
        return self.name

    def get_description(self):
        return f"{self.name} is an author from {self.country}."


class AuthorProfile(models.Model):
    author = models.OneToOneField(
        Author,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    bio = models.TextField()

    def __str__(self):
        return f"Profile for {self.author.name}"


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Book(models.Model):
    GENRE_CHOICES = [
        ("F", "Fiction"),
        ("NF", "Non-Fiction"),
        ("SF", "Science Fiction"),
        ("FAN", "Fantasy"),
        ("MYS", "Mystery"),
        ("THR", "Thriller"),
        ("ROM", "Romance"),
        ("HIS", "Historical"),
        ("BIO", "Biography"),
        ("SCI", "Science"),
        ("TEC", "Technology"),
    ]

    title = models.CharField(
        max_length=200,
        help_text="The book's full title"
    )
    subtitle = models.CharField(max_length=200, blank=True)
    isbn = models.CharField(
        max_length=13,
        unique=True,
        help_text="The book's unique 13-digit ISBN"
    )
    description = models.TextField(blank=True)
    summary = models.TextField(
        help_text="Brief description of the book",
        blank=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",
        null=True,
        blank=True
    )
    co_authors = models.ManyToManyField(
        Author,
        related_name="co_authored_books",
        blank=True
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books"
    )
    publication_date = models.DateField(null=True, blank=True)
    genre = models.CharField(
        max_length=3,
        choices=GENRE_CHOICES,
        default="F"
    )
    pages = models.IntegerField(
        validators=[MinValueValidator(1)],
        null=True,
        blank=True
    )
    cover_image = models.ImageField(
        upload_to="covers/",
        blank=True,
        null=True
    )
    language = models.CharField(max_length=50, default="English")
    is_available = models.BooleanField(default=True)
    borrowed_count = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    rating = models.IntegerField(
        default=3,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    categories = models.ManyToManyField(Category, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
