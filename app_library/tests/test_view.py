from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.test import TestCase
from django.urls import reverse
from app_library.models import AuthorModel, BookModel

NUMBERS_OF_AUTHOR = 3
NUMBERS_OF_BOOK = 3


class CreateAuthorAndBook(TestCase):
    """ Класс SetUp в котором создаются модели авторов и книг """
    COUNT_ISBN = 0

    @classmethod
    def setUpClass(cls):
        """ Классовый метод создания моделей авторов и книг """
        super().setUpClass()
        count_isbn = 0
        for i in range(NUMBERS_OF_AUTHOR):
            AuthorModel.objects.create(first_name=f'Author_first_name {i}',
                                       last_name=f'Author_last_name {i}',
                                       birthday=datetime.now().date())
            for j in range(NUMBERS_OF_BOOK):
                count_isbn += 1
                BookModel.objects.create(author=AuthorModel.objects.get(id=i+1),
                                         title=f'Test_title{j}',
                                         isbn=f'tests{count_isbn}',
                                         year_publication=datetime.now().year,
                                         num_pages=100)


class TestAuthorList(CreateAuthorAndBook):
    """ Класс тестирования списка авторов """

    def test_author_list_url_exists_at_desire_location(self):
        """ Метод тестирования url к списку авторов """

        response = self.client.get('/api/v1/library/author/')
        self.assertEqual(response.status_code, 200)

    def test_post_list_number(self):
        """ Метод тестирования сравнения созданных и отображаемых моделей авторов """

        response = self.client.get(reverse('author-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(int(AuthorModel.objects.count()) == NUMBERS_OF_AUTHOR)

    def test_post_create_author(self):
        """ Метод тестирования post запроса создания нового автора """

        response = self.client.post(reverse('author-list'), data={
            'first_name': 'PostTest1',
            'last_name': 'PostTest2',
            'birthday': datetime.now().date(),
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(int(AuthorModel.objects.count()) == NUMBERS_OF_AUTHOR+1)

    def test_author_list_filter_url_exists_at_desire_location(self):
        """ Метод тестирования get запроса фильтра по имени автора """

        response = self.client.get(
            '/api/v1/library/author/?first_name=Author_first_name 2&')
        self.assertEqual(response.status_code, 200)


class TestAuthorDetail(CreateAuthorAndBook):
    """ Класс тестирования отдельного автора """

    def test_author_detail_url_exists_at_desire_location(self):
        """ Метод тестирования url к конкретному автору """

        last_author_id = AuthorModel.objects.last().id
        response = self.client.get(f'/api/v1/library/author/{last_author_id}/')

    def test_put_list_number(self):
        """ Метод тестирования put запроса создания редактирования данных об автора """

        last_author = AuthorModel.objects.last()
        data = ({'first_name': 'PostTestPUT',
                 'last_name': 'PostTestPUT',
                 'birthday': datetime.now().date()-relativedelta(years=1)})
        response = self.client.patch(reverse('author-detail', kwargs={'pk': last_author.id}),
                                     data,
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)

        last_author_update = AuthorModel.objects.last()
        self.assertTrue(last_author.first_name != last_author_update.first_name)
        self.assertTrue(last_author.last_name != last_author_update.last_name)
        self.assertTrue(last_author.birthday != last_author_update.birthday)

    def test_delete_list_number(self):
        """ Метод тестирования delete запроса для удаления автора из списка модели"""

        last_author = AuthorModel.objects.last()
        response = self.client.delete(reverse('author-detail', kwargs={'pk': last_author.id}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertTrue(int(AuthorModel.objects.count()) == NUMBERS_OF_AUTHOR-1)


class TestBookList(CreateAuthorAndBook):
    """ Класс тестирования списка книг """

    def test_book_list_url_exists_at_desire_location(self):
        """ Метод тестирования url к списку книг """

        response = self.client.get('/api/v1/library/book/')
        self.assertEqual(response.status_code, 200)

    def test_book_list_number(self):
        """ Метод тестирования сравнения созданных и отображаемых моделей книг """

        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(int(BookModel.objects.count()) == NUMBERS_OF_BOOK*NUMBERS_OF_AUTHOR)

    def test_book_create_author(self):
        """ Метод тестирования post запроса создания новой книги """

        data = {'author': AuthorModel.objects.first().id,
                'title': 'TestTitlePost',
                'isbn': 'Test12',
                'year_publication': 1900,
                'num_pages': 5}
        response = self.client.post(reverse('book-list'), data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(int(BookModel.objects.count()) == NUMBERS_OF_BOOK*NUMBERS_OF_AUTHOR+1)

    def test_book_list_filter_url_exists_at_desire_location(self):
        """ Метод тестирования get запроса фильтра по имени автора и фамилии автора, заголовку и числу страниц """

        response = self.client.get(
            '/api/v1/library/book/?title=Test_title1&'
            'author_first_name=Author_first_name 2&'
            'author_last_name=Author_last_name 2&'
            'num_page=>5')
        self.assertEqual(response.status_code, 200)


class TestBookDetail(CreateAuthorAndBook):
    """ Класс тестирования отдельной книги """

    def test_book_detail_url_exists_at_desire_location(self):
        """ Метод тестирования url к конкретной книге """

        last_book = BookModel.objects.last()
        response = self.client.get(f'/api/v1/library/book/{last_book.id}/')
        self.assertEqual(response.status_code, 200)

    def test_put_book_detail_number(self):
        """ Метод тестирования put запроса создания редактирования данных об книге """

        last_book = BookModel.objects.last()
        data = {'author': AuthorModel.objects.first().id,
                'title': 'TestTitlePUT',
                'isbn': 'Test13',
                'year_publication': 1901,
                'num_pages': 6}
        response = self.client.patch(reverse('book-detail', kwargs={'pk': last_book.id}),
                                     data,
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)
        last_author_put = BookModel.objects.last()
        self.assertTrue(last_book.author != last_author_put.author)
        self.assertTrue(last_book.title != last_author_put.title)
        self.assertTrue(last_book.isbn != last_author_put.isbn)
        self.assertTrue(last_book.year_publication != last_author_put.year_publication)
        self.assertTrue(last_book.num_pages != last_author_put.num_pages)

    def test_delete_list_number(self):
        """ Метод тестирования delete запроса для удаления книги из списка модели"""

        last_book = BookModel.objects.last()
        response = self.client.delete(reverse('book-detail', kwargs={'pk': last_book.id}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertTrue(int(BookModel.objects.count()) == NUMBERS_OF_BOOK*NUMBERS_OF_AUTHOR-1)

