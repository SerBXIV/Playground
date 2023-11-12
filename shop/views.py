from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Genre, Book, Section
from cart.forms import CartAddBookForm


class BookListView(ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'shop/book/list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(available=True)
        genre_slug = self.kwargs.get('genre_slug')
        if genre_slug:
            queryset = queryset.filter(genre__slug=genre_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre'] = None
        genre_slug = self.kwargs.get('genre_slug')
        if genre_slug:
            context['genre'] = get_object_or_404(Genre, slug=genre_slug)
        context['genres'] = Genre.objects.all()
        context['sections'] = Section.objects.all()
        return context


class BookDetailView(DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'shop/book/detail.html'

    def get_queryset(self):
        return super().get_queryset().filter(available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_book_form'] = CartAddBookForm()
        context['book_author'] = self.object.authors.all()
        context['book_genre'] = self.object.genre.all()
        context['genres'] = Genre.objects.all()
        context['sections'] = Section.objects.all()
        return context
