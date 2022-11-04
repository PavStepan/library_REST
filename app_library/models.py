from django.db import models


class AuthorModel(models.Model):
    """ Модель таблицы авторов """

    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    birthday = models.DateField(verbose_name='Дата рождения')

    def get_name(self):
        """ Метод предоставления имя и фамилии автора """

        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        """ Метод строкового представления модели авторов """

        return f'{self.first_name} {self.last_name}'


class BookModel(models.Model):
    """ Модель таблицы книг """

    author = models.ForeignKey(AuthorModel, on_delete=models.CASCADE, related_name='author')
    author_first_last_name = models.CharField(max_length=100, blank=True, verbose_name='Имя и фамилия автора книги')
    title = models.CharField(max_length=100, verbose_name='Название книги')
    isbn = models.CharField(max_length=6, unique=True, verbose_name='Идентификатор книги')
    year_publication = models.PositiveIntegerField(verbose_name='Дата публикации книги')
    num_pages = models.PositiveIntegerField(verbose_name='Число страниц у книги')

    def __str__(self):
        """ Метод строкового представления модели книг """

        return self.title
