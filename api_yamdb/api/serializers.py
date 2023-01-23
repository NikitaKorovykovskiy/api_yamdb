from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, ValidationError

from reviews.models import Category, Genre, Title
from users.models import CustomUser


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий произведений."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров произведений."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для возврата списка произведений."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        many=True, 
        read_only=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year',
            'description', 'genre',
            'category'
        )
        read_only_fields = (
            'id', 'name', 'year',
            'description', 'genre',
            'category'
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления произведений."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
    )
    
    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year',
            'description', 'genre',
            'category'
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        ]
        validator = [
            UniqueTogetherValidator(
                queryset=CustomUser.objects.all(),
                fields=['username', 'email']
            )
        ]


class UserSignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
        validators = [
            UniqueTogetherValidator(
                queryset=CustomUser.objects.all(),
                fields=['username', 'email']
            )
        ]

    # def validate_username(self, value):
    #     if value.lower() == 'me':
    #         raise ValidationError('username не может быть "me"')
    #     return value
