from django.urls import path
from .views import home, BookDetailView, add_book, BookUpdateView, BookDeleteView, book_list, book_detail, book_search_ajax, book_toggle_availability

urlpatterns = [
    path("catalog/", book_list, name="book-list"),
    path("catalog/<int:pk>/", book_detail, name="book-detail-fbv"),
    path("search-ajax/", book_search_ajax, name="book-search-ajax"),
    path("books/<int:pk>/toggle-availability/", book_toggle_availability, name="book-toggle-availability"),
    path("", home, name="home"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("books/add/", add_book, name="add_book"),
    path("books/<int:pk>/edit/", BookUpdateView.as_view(), name="edit_book"),
    path("books/<int:pk>/delete/", BookDeleteView.as_view(), name="delete_book"),
]
