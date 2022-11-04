from rest_framework import serializers
from app_library.models import AuthorModel, BookModel


class AuthorSerializer(serializers.ModelSerializer):
    """ Класс сериализатор модели авторов """

    class Meta:
        model = AuthorModel
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    """ Класс сериализатор модели книги """

    author_first_last_name = serializers.CharField(source='author.get_name', read_only=True)

    class Meta:
        model = BookModel
        fields = '__all__'

