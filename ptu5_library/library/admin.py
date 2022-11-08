from django.contrib import admin
from . import models
# Register your models here.

class BookInstanceInline(admin.TabularInline):
    model = models.BookInstance
    extra = 0
    # readonly_fields = ('unique_id', )
    can_delete = False


class BookAdmin(admin.ModelAdmin):
    list_display  = ('title', 'author', 'display_genre')
    inlines = (BookInstanceInline,)


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'book', 'status', 'due_back')
    # sukuriam filtrus
    list_filter = ('status', 'due_back')
    readonly_fields = ('unique_id', )
    search_fields = ('unique_id', 'book__title', 'book__author__last_name',) # django lookup     +   __exact
    list_editable = ('status', 'due_back')

    fieldsets = (
    ('General', {'fields': ('unique_id', 'book')}),
    ('Availability', {'fields': (('status', 'due_back'),)}),
    ) # 'due_back'),) - sita kablelis ledzia isdelioti eilutes tvarka


class AuthorAdimn(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'display_books')
    list_display_links = ('last_name', )


admin.site.register(models.Author, AuthorAdimn)
admin.site.register(models.Genre)
admin.site.register(models.Book, BookAdmin)
admin.site.register(models.BookInstance, BookInstanceAdmin)
