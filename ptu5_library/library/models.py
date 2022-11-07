from django.db import models
import uuid

# Create your models here.
class Genre(models.Model):
    name = models.CharField('name', max_length = 200, help_text = 'Enter name of book genre')

    def __str__(self) -> str:
        return self.name


class Author(models.Model):
    first_name = models.CharField('first_name', max_length = 50)
    last_name = models.CharField('last_name', max_length = 50)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['last_name', 'first_name']


class Book(models.Model):
    title = models.CharField('title', max_length = 255) # string
    summery = models.TextField('summery') # didelis koda, sunku filtruoti ir ieskoti per tekst
    isbn = models.CharField('ISBN', max_length=12, null=True, blank=True, 
        help_text='<a href="https://www.isbn-international.org/content/what-isbn" target="_blank"> ISBN code</a>consisting of 13 symbols') # knygu kodas
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True) # PROTECT -neleidzia trinti, SETNULL - paliks be autoriu, CASCADE - istrins viska 
    genre = models.ManyToManyField(Genre, help_text='Choose genre(s) for this book', verbose_name='genre(s)')

    def __str__(self) -> str:
        return f"{self.author} - {self.title}"


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

    def __str__(self) -> str:
        return f"{self.unique_id} : {self.book.title}"

    class Meta:
        ordering = ['due_back']