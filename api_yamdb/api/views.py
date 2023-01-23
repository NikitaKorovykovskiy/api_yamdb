from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import Category, Genre, Title
from users.models import CustomUser

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permission import *
from .permission import IsAdminModeratorOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          UserSerializer, UserSignUpSerializer)
from .utils import make_confirmation_code


class CategoryViewSet(CreateListDestroyViewSet):
    """Отображение действий с категориями произведений."""

    queryset = Category.objects.all().order_by('-id')
    pagination_class = PageNumberPagination
    serializer_class = CategorySerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    """Отображение действий с жанрами произведений."""

    queryset = Genre.objects.all().order_by('-id')
    pagination_class = PageNumberPagination
    serializer_class = GenreSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]
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


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly,)
    serializer_class = UserSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'


class APISignup(APIView):
    pass
