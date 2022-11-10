from django.db import models
import uuid
from django.utils.html import format_html
from django.urls import reverse

# Create your models here.
class Genre(models.Model):
    name = models.CharField('name', max_length = 200, help_text = 'Enter name of book genre')

    def __str__(self) -> str:
        return self.name

    def link_filtered_books(self):
        link = reverse('books')+'?genre_id='+str(self.id)
        return format_html('<a class="genre" href="{link}">{name}</a>', link=link, name=self.name)


class Author(models.Model):
    first_name = models.CharField('first_name', max_length = 50)
    last_name = models.CharField('last_name', max_length = 50)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


    def display_books(self) -> str:
        return ', '.join(book.title for book in self.books.all())
    display_books.short_description = 'books'

    def link(self) -> str:
        link = reverse('author', kwargs={'author_id':self.id})
        return format_html('<a href="{link}">{author}</a>', link=link, author=self.__str__())

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'author'
        verbose_name_plural ='authors'


class Book(models.Model):
    title = models.CharField('title', max_length = 255) # string
    summery = models.TextField('summery') # didelis koda, sunku filtruoti ir ieskoti per tekst
    isbn = models.CharField('ISBN', max_length=12, null=True, blank=True, 
        help_text='<a href="https://www.isbn-international.org/content/what-isbn" target="_blank"> ISBN code</a>consisting of 13 symbols') # knygu kodas
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, 
    null=True, blank=True,
    related_name='books',) # PROTECT -neleidzia trinti, SETNULL - paliks be autoriu, CASCADE - istrins viska 
    genre = models.ManyToManyField(Genre, help_text='Choose genre(s) for this book', verbose_name='genre(s)')

    def __str__(self) -> str:
        return f"{self.author} - {self.title}"

    def display_genre(self) -> str:
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = 'genre(s)'

    # @property
    # def author_link(self) -> str:
    #     link = reverse('author', kwargs={'author_id': self.author.id})
    #     return format_html('<a href="{link}">{author}</a>', link=link, author=self.author)


class BookInstance(models.Model):
    unique_id = models.UUIDField('unique_id', default=uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, verbose_name="book", on_delete=models.CASCADE) 
    due_back = models.DateField('due back', null=True, blank=True)

    LOAN_STATUS = (
            ('m', 'managed'),
            ('t', 'taken'),
            ('a', 'availible'),
            ('r', 'reserved'),
    )

    status = models.CharField('status', max_length=1, choices=LOAN_STATUS, default='m')
    # price = models.DecimalField('price', max_digits=15, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.unique_id} : {self.book.title}"

    class Meta:
        ordering = ['due_back']