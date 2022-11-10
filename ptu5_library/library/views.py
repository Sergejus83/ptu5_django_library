from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DeleteView
from django.http import HttpResponse
from . models import Genre, Author, Book, BookInstance

# Create your views here.

def index(request):
    # return HttpResponse("Sveiki atvyke!")
    book_count = Book.objects.count()
    book_intance_count = BookInstance.objects.count()
    book_instance_availible_count = BookInstance.objects.filter(status='a').count()
    author_count = Author.objects.count()
    genre_count = Genre.objects.count()

    context = {
        'book_count': book_count,
        'book_intance_count': book_intance_count,
        'book_intance_availible': book_instance_availible_count,
        'author_count': author_count,
        'genre_count': genre_count,
    }

    return render(request, 'library/index.html', context)


def authors(request):
    return render(request, 'library/authors.html', {'authors': Author.objects.all()})

def author(request, author_id):
    return render(request, 'library/author.html', {'author': get_object_or_404(Author,id=author_id)})


class BookListView(ListView):
    model = Book
    template_name = 'library/book_list.html'

