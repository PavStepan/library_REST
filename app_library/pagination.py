from rest_framework.pagination import PageNumberPagination


class BookAPIListPagination(PageNumberPagination):
    """ Модель пагинации для представления модели книги """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000
