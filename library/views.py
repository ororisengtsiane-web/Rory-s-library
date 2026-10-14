from django.shortcuts import render
from django.views.generic import DetailView, UpdateView, DeleteView
from .models import Book
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookForm, BookSearchForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

def home(request):
    books = Book.objects.select_related("author", "publisher").all()
    search_form = BookSearchForm(request.GET or None)
    query = request.GET.get("q", "").strip()
    genre = request.GET.get("genre", "")
    sort = request.GET.get("sort", "title")
    if query:
        books = books.filter(Q(title__icontains=query) | Q(isbn__icontains=query) | Q(author__name__icontains=query))
    if genre:
        books = books.filter(genre=genre)
    allowed_sort = {"title", "-title", "-rating", "-publication_date", "publication_date"}
    books = books.order_by(sort if sort in allowed_sort else "title")
    page_obj = Paginator(books, 12).get_page(request.GET.get("page"))
    params = request.GET.copy()
    params.pop("page", None)
    return render(request, "library/home.html", {
        "books": page_obj.object_list, "page_obj": page_obj,
        "search_form": search_form, "query_params": params.urlencode(),
    })


class BookDetailView(DetailView):
    model = Book
    template_name = "library/book_detail.html"
    context_object_name = "book"

def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "Book saved successfully.")
            return redirect("home")
    else:
        form = BookForm()

    return render(request, "library/book_form.html", {
        "form": form
    })

class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = "library/book_form.html"
    context_object_name = "book"
    success_url = "/"

class BookDeleteView(DeleteView):
    model = Book
    template_name = "library/book_confirm_delete.html"
    context_object_name = "book"
    success_url = "/"



def book_list(request):
    """Additional function-based list view, sharing the original homepage."""
    return home(request)


def book_detail(request, pk):
    """Additional function-based detail view without removing the original CBV."""
    book = get_object_or_404(Book.objects.select_related("author", "publisher"), pk=pk)
    similar_books = Book.objects.filter(genre=book.genre).exclude(pk=book.pk).order_by("-rating")[:4]
    return render(request, "library/book_detail.html", {"book": book, "similar_books": similar_books})


def book_search_ajax(request):
    query = request.GET.get("q", "").strip()
    if len(query) < 2:
        return JsonResponse({"results": []})
    books = Book.objects.filter(Q(title__icontains=query) | Q(author__name__icontains=query)).select_related("author")[:10]
    return JsonResponse({"results": [{"id": book.pk, "title": book.title, "author": str(book.author) if book.author else ""} for book in books]})


@login_required
@require_POST
def book_toggle_availability(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.is_available = not book.is_available
    book.save(update_fields=["is_available"])
    return JsonResponse({"success": True, "is_available": book.is_available})
