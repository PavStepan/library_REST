from django.urls import path, include
from rest_framework import routers
from app_library.views import AuthorViewSet, BookViewSet


router_publisher = routers.SimpleRouter()
router_publisher.register(r'author', AuthorViewSet, basename='author')

router_book = routers.SimpleRouter()
router_book.register(r'book', BookViewSet, basename='book')

urlpatterns = [
    path('library/', include(router_publisher.urls)),
    path('library/', include(router_book.urls)),

]
