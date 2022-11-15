from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DeleteView, DetailView
from django.http import HttpResponse
from . models import Genre, Author, Book, BookInstance
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

def index(request):
    # return HttpResponse("Sveiki atvyke!")
    book_count = Book.objects.count()
    book_intance_count = BookInstance.objects.count()
    book_instance_availible_count = BookInstance.objects.filter(status='a').count()
    author_count = Author.objects.count()
    genre_count = Genre.objects.count()
    visits_count = request.session.get('visits_count', 1)
    request.session['visits_count'] = visits_count + 1

    context = {
        'book_count': book_count,
        'book_intance_count': book_intance_count,
        'book_intance_availible_count': book_instance_availible_count,
        'author_count': author_count,
        'genre_count': genre_count,
        'visits_count': visits_count,
    }

    return render(request, 'library/index.html', context)


def authors(request): 
    paginator = Paginator(Author.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)  
    return render(request, 'library/authors.html', {'authors': paged_authors})

def author(request, author_id):
    return render(request, 'library/author.html', {'author': get_object_or_404(Author,id=author_id)})


class BookListView(ListView):
    model = Book
    paginate_by = 2
    template_name = 'library/book_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('search')
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(summery__icontains=query))
        genre_id = self.request.GET.get('genre_id')
        if genre_id:
            queryset = queryset.filter(genre__id=genre_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['book_count'] = Book.objects.count()
        context['book_count'] = self.get_queryset().count()
        genre_id = self.request.GET.get('genre_id')
        context['genres']= Genre.objects.all()
        if genre_id:
            context['genre'] = get_object_or_404(Genre, id=genre_id)
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'library/book_detail.html'