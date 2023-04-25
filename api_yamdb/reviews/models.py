from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

from core.validators import validate_username, validate_year
from core.models import NameSlugModel, Note


USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = [
    (USER, 'Пользователь'),
    (ADMIN, 'Админ'),
    (MODERATOR, 'Модератор'),
]


class User(AbstractUser):
    username = models.SlugField(
        validators=(validate_username,),
        max_length=settings.NAME_LIMIT,
        unique=True,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        max_length=settings.EMAIL_LIMIT,
        unique=True,
        blank=False,
        null=False,
    )
    role = models.CharField(
        'роль',
        max_length=settings.ROLE_LIMIT,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True,
    )
    bio = models.TextField(
        'биография',
        blank=True,
    )
    first_name = models.CharField(
        'имя',
        max_length=settings.NAME_LIMIT,
        blank=True,
    )
    last_name = models.CharField(
        'фамилия',
        max_length=settings.NAME_LIMIT,
        blank=True,
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=settings.CODE_LIMIT,
        null=True,
        blank=False,
    )

    class Meta:
        ordering = ('first_name', 'last_name',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.is_superuser or self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR


class Genre(NameSlugModel):
    class Meta(NameSlugModel.Meta):
        default_related_name = 'genres'
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(NameSlugModel):
    class Meta(NameSlugModel.Meta):
        default_related_name = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    name = models.CharField(
        max_length=settings.NAME_GENRE_CATEGORY_TITLE_LIMIT,
        verbose_name='Название произведения',
        help_text='Название произведения',
    )
    year = models.PositiveSmallIntegerField(
        validators=(validate_year,),
        verbose_name='Год выпуска произведения',
        help_text='Год выпуска произведения',
        db_index=True
    )
    description = models.TextField(
        blank=True, null=True,
        verbose_name='Описание произведения',
        help_text='Описание произведения',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, null=True,
        related_name='title',
        verbose_name='Категория',
        help_text='Категория, к которой будет относиться произведение'
    )
    genre = models.ManyToManyField(Genre, related_name='title',
                                   verbose_name='Жанры',
                                   through='GenreTitle')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-year', 'name')
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, related_name='genre_title',
                              verbose_name='Жанр',
                              on_delete=models.CASCADE,
                              null=True)
    title = models.ForeignKey(Title, related_name='genre_title',
                              verbose_name='Произведение',
                              on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'

    class Meta:
        verbose_name = 'Жанр-Произведение'
        verbose_name_plural = 'Жанры-Произведения'


class Review(Note):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка',
        default=1
    )

    class Meta(Note.Meta):
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_author_title'
            )
        ]


class Comment(Note):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )

    class Meta(Note.Meta):
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
