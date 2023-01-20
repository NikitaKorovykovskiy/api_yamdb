from django.db import models

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
        max_length=200,
        help_text='Укажите название произведения'
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        help_text='Укажите год выпуска произведения'
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
