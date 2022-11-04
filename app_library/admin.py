from django.contrib import admin
from app_library.models import BookModel, AuthorModel
# Register your models here.


class BookAdmin(admin.ModelAdmin):
    """ Класс представления модели книг в админ панели """
    list_display = ['id', 'title']


class BookInLine(admin.TabularInline):
    """ Класс представления модели книг в виде таблицы авторов в админ панели """

    model = BookModel


class AuthorAdmin(admin.ModelAdmin):
    """ Класс представления модели авторов в админ панели """

    list_display = ['id', 'first_name', 'last_name']
    inlines = [BookInLine]


admin.site.register(AuthorModel, AuthorAdmin)
admin.site.register(BookModel, BookAdmin)

