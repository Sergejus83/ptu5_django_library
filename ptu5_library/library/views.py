from django.shortcuts import render
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

    
