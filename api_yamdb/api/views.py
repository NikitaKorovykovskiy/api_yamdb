from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import ADMIN_EMAIL
from reviews.models import Category, Genre, Title
from users.models import CustomUser

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permission import AuthorAdminModeratorOrReadOnly, IsAdmin, ReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          SignupSerializer, TitleReadSerializer,
                          TitleWriteSerializer, TokenSerializer,
                          UserSerializer)


class CategoryViewSet(CreateListDestroyViewSet):
    """Отображение действий с категориями произведений."""

    queryset = Category.objects.all().order_by('-id')
    pagination_class = PageNumberPagination
    serializer_class = CategorySerializer
    permission_classes = [AuthorAdminModeratorOrReadOnly]
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    """Отображение действий с жанрами произведений."""

    queryset = Genre.objects.all().order_by('-id')
    pagination_class = PageNumberPagination
    serializer_class = GenreSerializer
    permission_classes = [AuthorAdminModeratorOrReadOnly]
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для произведений.
    Для запросов на чтение используется TitleReadSerializer
    Для запросов на изменение используется TitleWriteSerializer
    """

    #  queryset = Title.objects.all()
    queryset = Title.objects.all().annotate(
        Avg('reviews__score')).order_by('name')
    permission_classes = [IsAdmin | ReadOnly]
    #  pagination_class = LimitOffsetPagination,
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filterset_class = TitleFilter
    search_fields = ['name', 'category', 'slug']

    def get_serializer_class(self):
        #  if self.action in ('create', 'update', 'partial_update'):
        #  return TitleWriteSerializer
        #  return TitleReadSerializer
        if self.action == 'retrieve' or self.action == 'list':
            return TitleReadSerializer
        return TitleWriteSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAdmin, )
    serializer_class = UserSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


SUBJECT = 'YaMDb: код подверждения'
MESSAGE = 'Ваш код подтверждения - {}'
FIELD_ERROR = 'Неуникальное поле. Пользователь с таким {} уже существует'


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, created = CustomUser.objects.get_or_create(
            email=serializer.validated_data['email'],
            username=serializer.validated_data['username'],
        )
    except IntegrityError as error:
        raise ValidationError(FIELD_ERROR.format(f'{error}'.partition('.')[2]))
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        SUBJECT,
        MESSAGE.format(confirmation_code),
        ADMIN_EMAIL,
        [user.email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        CustomUser,
        username=serializer.validated_data['username'],
    )
    if not default_token_generator.check_token(
            user,
            serializer.validated_data['confirmation_code']):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    token = AccessToken.for_user(user)
    data = {
        'token': str(token),
    }
    return Response(data)
