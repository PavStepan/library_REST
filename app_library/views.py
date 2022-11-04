from rest_framework import viewsets
from app_library.models import AuthorModel, BookModel
from app_library.pagination import BookAPIListPagination
from app_library.serializer import AuthorSerializer, BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """ Представление для получения списка авторов и предоставление детальной информации о каждой записи, а так же
     для редактирования, удаления и добавления записи """

    serializer_class = AuthorSerializer

    def get_queryset(self):
        """ Метод отображения отфильтрованного списка модели книг """

        queryset = AuthorModel.objects.all()
        author_name = self.request.query_params.get('first_name')
        if author_name:
            queryset = queryset.filter(first_name=author_name)
        return queryset


class BookViewSet(viewsets.ModelViewSet):
    """ Представление для получения списка книг и предоставление детальной информации о каждой записи, а так же
     для редактирования, удаления и добавления записи """

    serializer_class = BookSerializer
    pagination_class = BookAPIListPagination

    def get_queryset(self):
        """ Метод отображения отфильтрованного списка модели книг """

        queryset = BookModel.objects.all()
        title = self.request.query_params.get('title')
        author_first_name = self.request.query_params.get('author_first_name')
        author_last_name = self.request.query_params.get('author_last_name')

        if author_first_name:
            queryset = queryset.filter(author__first_name=author_first_name)
        if author_last_name:
            queryset = queryset.filter(author__last_name=author_last_name)
        if title:
            queryset = queryset.filter(title__icontains=title)

        num_page = self.request.query_params.get('num_page')

        if num_page:
            if num_page[0] == '>' and num_page[1:].isdigit():
                queryset = queryset.filter(num_pages__gt=int(num_page[1:]))
            elif num_page[0] == '<' and num_page[1:].isdigit():
                queryset = queryset.filter(num_pages__lt=int(num_page[1:]))
            elif num_page.isdigit():
                queryset = queryset.filter(num_pages=int(num_page))

        return queryset
