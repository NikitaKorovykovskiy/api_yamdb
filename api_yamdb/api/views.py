from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets

from .mixins import CreateListDestroyViewSet
from reviews.models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleReadSerializer, TitleWriteSerializer
from .permission import IsAdminOrReadOnly
from .filters import TitleFilter

class CategoryViewSet(CreateListDestroyViewSet):
    """Отображение действий с категориями произведений."""

    queryset = Category.objects.all().order_by('-id')
    pagination_class = PageNumberPagination
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    """Отображение действий с жанрами произведений."""

    queryset = Genre.objects.all().order_by('-id')
    pagination_class = PageNumberPagination
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для произведений.
    Для запросов на чтение используется TitleReadSerializer
    Для запросов на изменение используется TitleWriteSerializer
    """

    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleWriteSerializer
        return TitleReadSerializer