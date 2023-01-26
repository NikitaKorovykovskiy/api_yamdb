from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import CustomUser
from reviews.validators import validate_year


class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        max_length=150,
        unique=True,
        help_text='Укажите категорию'
    )
    slug = models.SlugField(
        verbose_name='Уникальный идентификатор',
        max_length=50,
        unique=True,
        help_text='Укажите уникальный идентификатор категории'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр',
        max_length=150,
        unique=True,
        help_text='Укажите жанр'
    )
    slug = models.SlugField(
        verbose_name='Уникальный идентификатор',
        max_length=50,
        unique=True,
        help_text='Укажите уникальный идентификатор жанра'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256,
        help_text='Укажите название произведения'
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        help_text='Укажите год выпуска произведения',
        validators=(validate_year,),
    )
    description = models.TextField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
        help_text='Укажите жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        max_length=200,
        blank=True,
        null=True,
        related_name='titles',
        help_text='Укажите категорию',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(max_length=200)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
