from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from .mixins import CreateListDestroyViewSet
from reviews.models import Category, Genre
from .serializers import CategorySerializer, GenreSerializer
#  from .permissions import IsAdminOrReadOnly

class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all().order_by('-id')
    pagination_class = PageNumberPagination
    serializer_class = CategorySerializer
    #  permission_classes = [IsAdminOrReadOnly]
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all().order_by('-id')
    pagination_class = PageNumberPagination
    serializer_class = GenreSerializer
    #  permission_classes = [IsAdminOrReadOnly]
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'